"""Camera inputs and guided, quality-checked face enrollment."""

import shutil
import time
import urllib.request
import uuid
from urllib.parse import urlparse, urlunparse

import cv2
import numpy as np

from .config import CASCADE_PATH, FACES_DIR, SAMPLES_PER_PERSON

CONNECTION_TIMEOUT_SECONDS = 20
RETRY_DELAY_SECONDS = 0.4
_DIRECT_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _show_waiting(window, title, details=""):
    """Show connection progress while a camera has not returned a frame yet."""
    frame = np.full((480, 900, 3), (38, 53, 73), dtype=np.uint8)
    cv2.rectangle(frame, (0, 0), (900, 8), (166, 177, 22), -1)
    cv2.putText(
        frame, "CAMPUSFLOW CAMERA", (42, 78), cv2.FONT_HERSHEY_SIMPLEX,
        0.75, (220, 236, 248), 2, cv2.LINE_AA,
    )
    cv2.putText(
        frame, title[:62], (42, 172), cv2.FONT_HERSHEY_SIMPLEX,
        0.9, (255, 255, 255), 2, cv2.LINE_AA,
    )

    lines = []
    for paragraph in str(details).splitlines():
        words, line = paragraph.split(), ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if len(candidate) > 68 and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)

    for index, line in enumerate(lines[:5]):
        cv2.putText(
            frame, line, (42, 232 + index * 34), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (190, 207, 225), 1, cv2.LINE_AA,
        )
    cv2.putText(
        frame,
        "Press Q to cancel. IP Webcam needs the same Wi-Fi as this computer.",
        (42, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (125, 223, 214),
        1,
        cv2.LINE_AA,
    )
    cv2.imshow(window, frame)
    key = cv2.waitKey(1)
    return key & 0xFF if key >= 0 else -1


def _wait_with_status(window, title, details, stop, seconds):
    """Keep the camera window responsive while waiting between retries."""
    deadline = time.monotonic() + seconds
    while not stop.is_set() and time.monotonic() < deadline:
        if _show_waiting(window, title, details) == ord("q"):
            stop.set()
            return False
        stop.wait(0.1)
    return not stop.is_set()


def _connection_advice(kind, url, error):
    """Turn common camera connection errors into a useful next step."""
    if kind != "IP Webcam":
        return (
            "Check Windows camera privacy settings and close other apps "
            "that may be using the camera."
        )

    address = url or "the entered phone address"
    message = str(error or "").lower()
    if "10061" in message or "refused" in message:
        return (
            f"No camera server is listening at {address}. Start IP Webcam "
            "on the phone and confirm the current address and port."
        )
    if "timed out" in message or "10060" in message:
        return (
            f"No reply came from {address}. Put the phone and computer on "
            "the same Wi-Fi and check the phone's current address."
        )
    return (
        f"CampusFlow could not read an image from {address}. Start IP Webcam, "
        "check its current address, and try the /shot.jpg page on this computer."
    )


def discard_samples(person_id):
    folder = FACES_DIR / person_id
    if folder.exists():
        shutil.rmtree(folder)


class Source:
    """Read frames from a local camera or an IP Webcam URL."""

    def __init__(self, kind, value):
        self.kind = kind
        self.cap = None
        self.last_error = None
        self.url = None
        self.notice = None

        if kind == "System camera":
            self.cap = cv2.VideoCapture(int(value or 0))
            if not self.cap.isOpened():
                self.cap.release()
                raise RuntimeError(
                    "System camera unavailable. Check its index or connection."
                )
            return

        url = value.strip()
        if not url:
            raise ValueError("Enter the IP Webcam URL.")
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        parsed = urlparse(url)
        path = parsed.path.rstrip("/").lower()
        if path.endswith(("/video", "/videofeed", "/mjpegfeed")):
            self.url = url
            self.cap = cv2.VideoCapture(
                url,
                cv2.CAP_FFMPEG,
                [
                    cv2.CAP_PROP_OPEN_TIMEOUT_MSEC,
                    5000,
                    cv2.CAP_PROP_READ_TIMEOUT_MSEC,
                    5000,
                ],
            )
            if not self.cap.isOpened():
                self.cap.release()
                self.cap = None
                # IP Webcam also serves still JPEGs if OpenCV cannot open MJPEG.
                fallback_path = parsed.path.rstrip("/").rsplit("/", 1)[0] + "/shot.jpg"
                self.url = urlunparse(
                    parsed._replace(path=fallback_path, query="", fragment="")
                )
                self.notice = (
                    "The video stream could not open. Trying the snapshot endpoint."
                )
        elif path.endswith((".jpg", ".jpeg", ".png")):
            self.url = url
        else:
            # A base address such as http://192.168.1.10:8080 uses /shot.jpg.
            self.url = url.rstrip("/") + "/shot.jpg"

    def read(self):
        if self.cap is not None:
            ok, frame = self.cap.read()
            self.last_error = (
                None if ok else "The camera stream did not return a frame."
            )
            return ok, frame

        try:
            request = urllib.request.Request(
                self.url, headers={"User-Agent": "CampusFlow/1.0"}
            )
            # Phone camera URLs are local-network devices. Bypass configured
            # HTTP proxies so requests go directly to the phone.
            with _DIRECT_OPENER.open(request, timeout=4) as response:
                data = np.frombuffer(response.read(), np.uint8)
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            self.last_error = (
                None
                if frame is not None
                else "The URL did not return a readable image."
            )
            return frame is not None, frame
        except Exception as exc:
            self.last_error = str(exc)
            return False, None

    def close(self):
        if self.cap is not None:
            self.cap.release()


def capture(name, role, kind, value, status):
    """Collect 100 clear face crops, then return a new profile ID."""
    status("Connecting to camera and checking its image…")
    source = None
    source_url = value.strip() if kind == "IP Webcam" else None
    person_id = uuid.uuid4().hex
    folder = FACES_DIR / person_id
    folder.mkdir(parents=True, exist_ok=False)
    detector = cv2.CascadeClassifier(str(CASCADE_PATH))
    count = 0
    next_capture_at = 0.0
    last_frame_at = time.monotonic()
    last_wait_status_at = 0.0
    last_feedback_at = 0.0
    connected_message_sent = False
    last_error = None

    if detector.empty():
        folder.rmdir()
        raise RuntimeError("Face detector file is missing.")

    window = "CampusFlow | Guided face setup"
    try:
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window, 900, 480)
        _show_waiting(
            window,
            "Connecting to camera...",
            source_url or f"System camera index {value or 0}",
        )

        while count < SAMPLES_PER_PERSON:
            if source is None:
                try:
                    source = Source(kind, value)
                    source_url = source.url or source_url
                    if source.notice:
                        status(source.notice)
                        _show_waiting(window, "Trying another camera mode", source.notice)
                except Exception as exc:
                    last_error = str(exc)
                    if time.monotonic() - last_wait_status_at >= 1:
                        status(f"Camera unavailable: {last_error} • retrying…")
                        last_wait_status_at = time.monotonic()
                    key = _show_waiting(window, "Camera unavailable; retrying…", last_error)
                    if key == ord("q"):
                        raise RuntimeError("Capture cancelled. No registration was saved; you can try again.")
                    if time.monotonic() - last_frame_at >= CONNECTION_TIMEOUT_SECONDS:
                        raise RuntimeError(
                            f"Could not open the camera after {CONNECTION_TIMEOUT_SECONDS} seconds. Check the selected camera and try again. Details: {last_error}"
                        )
                    time.sleep(0.2)
                    continue

            ok, frame = source.read()
            if not ok or frame is None:
                last_error = source.last_error or "No image received."
                if time.monotonic() - last_wait_status_at >= 1:
                    status("Waiting for a readable camera image…")
                    last_wait_status_at = time.monotonic()

                key = _show_waiting(
                    window,
                    "Waiting for a readable camera image…",
                    (
                        f"URL: {source.url or 'system camera'}\n{last_error}\n"
                        f"{_connection_advice(kind, source.url, last_error)}"
                    ),
                )
                if key == ord("q"):
                    raise RuntimeError(
                        "Capture cancelled. No registration was saved; you can try again."
                    )

                if time.monotonic() - last_frame_at >= CONNECTION_TIMEOUT_SECONDS:
                    detail = _connection_advice(kind, source.url, last_error)
                    if last_error:
                        detail += f" Connection detail: {last_error}"
                    _show_waiting(window, "Camera connection timed out", detail)
                    raise RuntimeError(detail)
                time.sleep(RETRY_DELAY_SECONDS)
                continue

            last_frame_at = time.monotonic()
            if not connected_message_sent:
                status("Camera connected. Looking for one clear face…")
                connected_message_sent = True

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.15, 6, minSize=(80, 80))
            view = frame.copy()
            tip = "Show one clear face"
            color = (0, 0, 255)

            if len(faces) == 1:
                x, y, w, h = faces[0]
                crop = gray[y : y + h, x : x + w]
                sharpness = cv2.Laplacian(crop, cv2.CV_64F).var()
                if sharpness < 45:
                    tip = "Blurry - hold still"
                elif time.monotonic() < next_capture_at:
                    tip = "Hold this angle"
                    color = (0, 180, 220)
                else:
                    face = cv2.equalizeHist(cv2.resize(crop, (100, 100)))
                    image_path = folder / f"{count:03d}.jpg"
                    if not cv2.imwrite(str(image_path), face):
                        raise RuntimeError(
                            "Could not save face image. Check folder permissions."
                        )
                    count += 1
                    status(
                        f"{count}/{SAMPLES_PER_PERSON} clear samples • "
                        "keep following the face-angle prompts"
                    )
                    next_capture_at = time.monotonic() + 0.45
                    tip = "Clear image accepted"
                    color = (0, 220, 0)
                cv2.rectangle(view, (x, y), (x + w, y + h), color, 2)
            elif len(faces) > 1:
                tip = "Only one person should be in frame"

            if count < 40:
                angle = "Look straight at camera"
            elif count < 55:
                angle = "Turn slightly to your left"
            elif count < 70:
                angle = "Turn slightly to your right"
            elif count < 85:
                angle = "Look slightly upward"
            elif count < SAMPLES_PER_PERSON:
                angle = "Look slightly downward"
            else:
                angle = "Capture complete"

            if time.monotonic() - last_feedback_at >= 1:
                status(f"{count}/{SAMPLES_PER_PERSON} clear samples • {tip} • {angle}")
                last_feedback_at = time.monotonic()

            cv2.putText(
                view, f"Clear samples {count}/{SAMPLES_PER_PERSON}", (12, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
            )
            cv2.putText(
                view, angle, (12, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                (0, 255, 255), 2,
            )
            cv2.putText(
                view, tip, (12, 86), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (0, 255, 255), 2,
            )
            cv2.putText(
                view, "Q cancels; rejected frames are not saved", (12, 112),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1,
            )
            cv2.imshow(window, view)
            status(f"{count}/{SAMPLES_PER_PERSON} clear samples • {angle} • {tip}")
            if cv2.waitKey(1) & 0xFF == ord("q"):
                raise RuntimeError(
                    "Capture cancelled. No registration was saved; you can try again."
                )
    except Exception:
        for image_path in folder.glob("*.jpg"):
            image_path.unlink(missing_ok=True)
        folder.rmdir()
        raise
    finally:
        if source is not None:
            source.close()
        try:
            cv2.destroyWindow(window)
        except cv2.error:
            pass

    if len(list(folder.glob("*.jpg"))) != SAMPLES_PER_PERSON:
        for image_path in folder.glob("*.jpg"):
            image_path.unlink(missing_ok=True)
        folder.rmdir()
        raise RuntimeError("Capture incomplete. Please try registration again.")

    return person_id
