import json
import time

import cv2
import numpy as np
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from keras.models import Sequential, load_model
from keras.optimizers import Adam

from .camera import Source, _connection_advice, _show_waiting, _wait_with_status
from .config import (
    BASE_DIR,
    CASCADE_PATH,
    CONFIDENCE_THRESHOLD,
    FACES_DIR,
    LABELS_PATH,
    MODEL_PATH,
)
from .storage import ensure_today_rows, list_people, mark, refresh_exports


def train(status):
    people = list_people()
    if len(people) < 2:
        raise RuntimeError(
            "At least two registered people are needed to train recognition."
        )
    x = []
    y = []
    for i, (pid, name, role) in enumerate(people):
        files = list((FACES_DIR / pid).glob("*.jpg"))
        if len(files) < 10:
            raise RuntimeError(f"{name} has too few saved face images. Register again.")
        for path in files:
            a = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if a is not None:
                a = cv2.equalizeHist(cv2.resize(a, (100, 100))).astype("float32") / 255
                x.append(a.reshape(100, 100, 1))
                y.append(i)
    if len(set(y)) < 2:
        raise RuntimeError("Need clear image samples from at least two people.")
    x = np.asarray(x, dtype="float32")
    y = np.asarray(y, dtype="int32")
    order = np.random.default_rng(42).permutation(len(x))
    x, y = x[order], y[order]
    model = Sequential(
        [
            Conv2D(24, (5, 5), activation="relu", input_shape=(100, 100, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(16, (3, 3), activation="relu"),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation="relu"),
            Dense(len(people), activation="softmax"),
        ]
    )
    model.compile(
        Adam(learning_rate=0.001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    status(f"Training model for {len(people)} people…")
    model.fit(x, y, validation_split=0.1, epochs=12, batch_size=16, verbose=0)
    model.save(MODEL_PATH)
    LABELS_PATH.write_text(
        json.dumps(
            [{"person_id": p[0], "name": p[1], "role": p[2]} for p in people],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return len(people)


def duplicate_face(person_id):
    """Return a registered profile only for a very strong model match across samples."""
    if not MODEL_PATH.exists() or not LABELS_PATH.exists():
        return None
    labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    model = load_model(MODEL_PATH)
    paths = sorted((FACES_DIR / person_id).glob("*.jpg"))
    if len(paths) < 20:
        return None
    indexes = np.linspace(0, len(paths) - 1, 20, dtype=int)
    votes = {}
    for index in indexes:
        image = cv2.imread(str(paths[int(index)]), cv2.IMREAD_GRAYSCALE)
        if image is None:
            continue
        image = (
            cv2.equalizeHist(cv2.resize(image, (100, 100)))
            .astype("float32")
            .reshape(1, 100, 100, 1)
            / 255
        )
        result = model.predict(image, verbose=0)[0]
        best = int(np.argmax(result))
        score = float(result[best])
        if score >= 0.98 and best < len(labels):
            votes[best] = votes.get(best, 0) + 1
    if votes:
        best, count = max(votes.items(), key=lambda item: item[1])
        if count >= 18:
            return labels[best]
    return None


def scan(mode, kind, value, stop, status, role_filter=None, frame_callback=None):
    detector = cv2.CascadeClassifier(str(CASCADE_PATH))
    model = load_model(MODEL_PATH)
    labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    source = None
    today = None
    last_notices = {}
    window = f"CampusFlow | {mode.title()} camera"
    if detector.empty():
        raise RuntimeError("Face detector file is missing.")
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window, 900, 480)
    if _show_waiting(
        window,
        f"Connecting to {mode} camera...",
        "Starting camera connection",
    ) == ord("q"):
        stop.set()
    try:
        while not stop.is_set():
            if source is None:
                try:
                    source = Source(kind, value)
                except Exception as e:
                    advice = _connection_advice(kind, value, e)
                    status(f"Camera unavailable: {e}; retrying in 3 seconds…")
                    if not _wait_with_status(
                        window,
                        "Camera unavailable; retrying…",
                        f"{e}\n{advice}",
                        stop,
                        3,
                    ):
                        break
                    continue
                if source.notice:
                    status(source.notice)
                    if _show_waiting(
                        window, "Using IP Webcam snapshot fallback", source.url
                    ) == ord("q"):
                        stop.set()
                        break
            day = __import__("datetime").datetime.now().strftime("%Y-%m-%d")
            if day != today:
                ensure_today_rows(day)
                refresh_exports()
                today = day
            ok, frame = source.read()
            if not ok or frame is None:
                error = source.last_error or "No frame received"
                detail = (
                    f"URL: {source.url or 'system camera'}\n{error}\n"
                    f"{_connection_advice(kind, source.url, error)}"
                )
                status(f"Camera feed lost; reconnecting in 2 seconds… {source.last_error or ''}")
                if not _wait_with_status(
                    window, "Camera feed lost; reconnecting…", detail, stop, 2
                ):
                    break
                source.close()
                source = None
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.2, 6, minSize=(60, 60))
            for x0, y0, w, h in faces:
                face = (
                    cv2.equalizeHist(
                        cv2.resize(gray[y0 : y0 + h, x0 : x0 + w], (100, 100))
                    )
                    .astype("float32")
                    .reshape(1, 100, 100, 1)
                    / 255
                )
                prob = model.predict(face, verbose=0)[0]
                ix = int(np.argmax(prob))
                score = float(prob[ix])
                margin = (
                    score - float(np.partition(prob, -2)[-2]) if len(prob) > 1 else 0.0
                )
                if (
                    score >= CONFIDENCE_THRESHOLD
                    and margin >= 0.15
                    and ix < len(labels)
                ):
                    person = labels[ix]
                    if (
                        role_filter in ("Student", "Faculty")
                        and person["role"] != role_filter
                    ):
                        msg = f"{person['role']} - not in this scan"
                        color = (230, 160, 30)
                    else:
                        added, msg = mark(person["person_id"], mode)
                        color = (0, 180, 80)
                        key = (person["person_id"], msg)
                        now = time.monotonic()
                        if added or now - last_notices.get(key, 0) > 5:
                            status(f"{person['name']} ({person['role']}): {msg}")
                            last_notices[key] = now
                    label = f"{person['name']} | {msg}"
                else:
                    label = f"Unknown {score:.0%}"
                    color = (0, 0, 255)
                cv2.rectangle(frame, (x0, y0), (x0 + w, y0 + h), color, 2)
                cv2.putText(
                    frame,
                    label,
                    (x0, max(20, y0 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )
            if frame_callback is not None:
                frame_callback(frame.copy())
            cv2.imshow(window, frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                stop.set()
    finally:
        if source is not None:
            source.close()
        try:
            cv2.destroyWindow(window)
        except cv2.error:
            pass
