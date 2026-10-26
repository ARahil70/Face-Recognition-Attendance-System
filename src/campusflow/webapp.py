import json
import re
import shutil
import threading
import urllib.parse
import uuid
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import storage
from .camera import capture, discard_samples
from .config import BASE_DIR, FACES_DIR, LABELS_PATH, MODEL_PATH, SAMPLES_PER_PERSON
from .recognition import duplicate_face, scan, train

WEB = Path(__file__).parent / "web"
_state = {
    "scan": None,
    "stop": None,
    "training": False,
    "training_error": None,
    "registration": None,
}
_training_lock = threading.Lock()
_registration_lock = threading.Lock()


def _registration_active():
    job = _state.get("registration")
    return bool(job and job.get("status") in ("connecting", "capturing", "saving"))


def _update_registration(job_id, **updates):
    with _registration_lock:
        job = _state.get("registration")
        if job and job.get("id") == job_id:
            job.update(updates)


def _model_is_current():
    try:
        labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
        current = {person[0] for person in storage.list_people()}
        return (
            len(current) >= 2
            and MODEL_PATH.exists()
            and {item["person_id"] for item in labels} == current
        )
    except Exception:
        return False


def _start_training():
    with _training_lock:
        if _state["training"]:
            return True
        if len(storage.list_people()) < 2:
            return False
        _state.update(training=True, training_error=None)

    def work():
        succeeded = False
        try:
            train(lambda _: None)
            succeeded = True
            _state["training_error"] = None
        except Exception as exc:
            _state["training_error"] = str(exc)
        finally:
            _state["training"] = False
            # A registration or deletion may have changed the roster during training.
            if succeeded and not _model_is_current():
                MODEL_PATH.unlink(missing_ok=True)
                LABELS_PATH.unlink(missing_ok=True)
                if len(storage.list_people()) >= 2:
                    _start_training()

    threading.Thread(target=work, daemon=True).start()
    return True


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, *a):
        pass

    def send(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith("/api/"):
            storage.initialize()
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            day = qs.get("date", [datetime.now().strftime("%Y-%m-%d")])[0]
            with storage.connect() as con:
                people = con.execute(
                    "SELECT p.person_id,p.name,p.role,p.created_at,COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'') FROM people p LEFT JOIN profile_details d USING(person_id) WHERE p.deleted_at IS NULL ORDER BY p.name"
                ).fetchall()
                # Build a date-accurate roster: people registered after the selected day
                # must not appear as absent in historical reports.
                existing = con.execute(
                    "SELECT person_id,name,role FROM people WHERE deleted_at IS NULL AND substr(created_at,1,10)<=?",
                    (day,),
                ).fetchall()
                con.executemany(
                    "INSERT OR IGNORE INTO attendance(day,person_id,name,role,first_seen,status,exit_time) VALUES(?,?,?,?,?,'A',NULL)",
                    [(day, *p, "") for p in existing],
                )
                rows = con.execute(
                    "SELECT a.day,a.name,a.role,a.status,a.first_seen,COALESCE(a.exit_time,''),COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'') FROM attendance a JOIN people p USING(person_id) LEFT JOIN profile_details d USING(person_id) WHERE a.day=? AND p.deleted_at IS NULL ORDER BY a.role,a.name",
                    (day,),
                ).fetchall()
                history = con.execute(
                    "SELECT a.day,a.person_id,a.name,a.role,a.status,a.first_seen,COALESCE(a.exit_time,''),COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'') FROM attendance a LEFT JOIN profile_details d USING(person_id) ORDER BY a.day DESC,a.name COLLATE NOCASE"
                ).fetchall()
            deleted_people = storage.list_deleted_people()
            return self.send(
                {
                    "people": people,
                    "deleted_people": deleted_people,
                    "records": rows,
                    "history": history,
                    "model_ready": _model_is_current(),
                    "training": _state["training"],
                    "training_error": _state["training_error"],
                    "registration": dict(_state["registration"])
                    if _state.get("registration")
                    else None,
                    "waiting_for_people": len(people) < 2,
                    "scanning": bool(_state["scan"]),
                    "scan_status": _state.get("scan_status", ""),
                    "scan_error": _state.get("error"),
                }
            )
        return super().do_GET()

    def do_POST(self):
        try:
            data = json.loads(
                self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}"
            )
            action = data.get("action")
            if action == "register":
                name = data["name"].strip()
                role = data["role"]
                kind = data.get("camera", "System camera")
                source = data.get("source", "0")
                if not name or role not in ("Student", "Faculty"):
                    return self.send({"error": "Enter a name and valid role."}, 400)
                if _state.get("scan"):
                    return self.send(
                        {
                            "error": "Stop the active camera scan before registering a new face."
                        },
                        409,
                    )
                if _registration_active():
                    return self.send(
                        {"error": "A face registration is already running. Wait for it to finish."},
                        409,
                    )
                with storage.connect() as con:
                    if con.execute(
                        "SELECT 1 FROM people WHERE lower(name)=lower(?) AND role=?",
                        (name, role),
                    ).fetchone():
                        return self.send(
                            {"error": "This name is already registered for this role."},
                            409,
                        )
                job_id = uuid.uuid4().hex
                with _registration_lock:
                    if _registration_active():
                        return self.send(
                            {"error": "A face registration is already running. Wait for it to finish."},
                            409,
                        )
                    _state["registration"] = {
                        "id": job_id,
                        "name": name,
                        "status": "connecting",
                        "message": "Starting camera connection…",
                        "count": 0,
                        "total": SAMPLES_PER_PERSON,
                        "percent": 0,
                    }

                details = {
                    "institution": "Mewar University",
                    "course": data.get("course", ""),
                    "branch": data.get("branch", ""),
                    "section": data.get("section", ""),
                }

                def work():
                    try:
                        def report(message):
                            match = re.search(r"(\d+)/(\d+) clear samples", message)
                            updates = {"message": message}
                            if match:
                                count, total = map(int, match.groups())
                                updates.update(
                                    status="capturing",
                                    count=count,
                                    total=total,
                                    percent=round(count * 100 / max(total, 1)),
                                )
                            elif message.startswith("Camera connected"):
                                updates["status"] = "capturing"
                            elif message.startswith("Waiting for"):
                                updates["status"] = "connecting"
                            _update_registration(job_id, **updates)

                        person_id = capture(name, role, kind, source, report)
                        samples_saved = False
                        try:
                            _update_registration(
                                job_id,
                                status="saving",
                                count=SAMPLES_PER_PERSON,
                                total=SAMPLES_PER_PERSON,
                                percent=100,
                                message="Checking the face samples before saving the profile…",
                            )
                            duplicate = (
                                duplicate_face(person_id)
                                if _model_is_current()
                                else None
                            )
                            if duplicate:
                                raise RuntimeError(
                                    f"This face strongly matches {duplicate['name']} "
                                    f"({duplicate['role']}). No second profile was saved."
                                )
                            storage.register_person(person_id, name, role, details)
                            samples_saved = True
                        finally:
                            if not samples_saved:
                                discard_samples(person_id)
                        MODEL_PATH.unlink(missing_ok=True)
                        LABELS_PATH.unlink(missing_ok=True)
                        started = _start_training()
                        message = (
                            "Registration complete. Recognition model is updating automatically."
                            if started
                            else "Registration complete. The model will update automatically after one more person is registered."
                        )
                        _update_registration(
                            job_id,
                            status="complete",
                            message=message,
                            person_id=person_id,
                        )
                    except Exception as exc:
                        _update_registration(
                            job_id,
                            status="error",
                            message=str(exc),
                        )

                threading.Thread(target=work, daemon=True).start()
                return self.send(
                    {
                        "ok": True,
                        "message": "Camera registration started. Live progress will appear here.",
                        "registration_id": job_id,
                    },
                    202,
                )
            if action == "train":
                started = _start_training()
                return self.send(
                    {
                        "ok": True,
                        "message": (
                            "Recognition model update started."
                            if started
                            else "Register at least two people; the model will then update automatically."
                        ),
                    }
                )
            if action == "update_profile":
                person_id = str(data.get("person_id", ""))
                with storage.connect() as con:
                    if not con.execute(
                        "SELECT 1 FROM people WHERE person_id=? AND deleted_at IS NULL",
                        (person_id,),
                    ).fetchone():
                        return self.send({"error": "Person was not found."}, 404)
                    con.execute(
                        "INSERT OR REPLACE INTO profile_details(person_id,institution,course,branch,section) VALUES(?,?,?,?,?)",
                        (
                            person_id,
                            "Mewar University",
                            str(data.get("course", "")),
                            str(data.get("branch", "")),
                            str(data.get("section", "")),
                        ),
                    )
                storage.refresh_exports()
                return self.send(
                    {
                        "ok": True,
                        "message": "Academic details saved. Face model does not need an update for course or section changes.",
                    }
                )
            if action == "delete_person":
                if _state.get("scan"):
                    return self.send(
                        {
                            "error": "Stop the active camera scan before deleting a profile."
                        },
                        409,
                    )
                person_id = str(data.get("person_id", ""))
                if not re.fullmatch(r"[a-f0-9]{32}", person_id):
                    return self.send({"error": "Invalid profile ID."}, 400)
                with storage.connect() as con:
                    row = con.execute(
                        "SELECT name FROM people WHERE person_id=? AND deleted_at IS NULL",
                        (person_id,),
                    ).fetchone()
                    if not row:
                        return self.send({"error": "Person was not found."}, 404)
                    con.execute(
                        "UPDATE people SET deleted_at=? WHERE person_id=?",
                        (datetime.now().isoformat(timespec="seconds"), person_id),
                    )
                MODEL_PATH.unlink(missing_ok=True)
                LABELS_PATH.unlink(missing_ok=True)
                storage.refresh_exports()
                started = _start_training()
                msg = "Profile moved to the Recycle Bin. Face samples and attendance history are preserved."
                if started:
                    msg += " The recognition model is updating automatically."
                elif len(storage.list_people()) < 2:
                    msg += (
                        " Register or restore another person before using recognition."
                    )
                return self.send({"ok": True, "message": f"{row[0]}: {msg}"})
            if action == "restore_person":
                if _state.get("scan"):
                    return self.send(
                        {
                            "error": "Stop the active camera scan before restoring a profile."
                        },
                        409,
                    )
                person_id = str(data.get("person_id", ""))
                if not re.fullmatch(r"[a-f0-9]{32}", person_id):
                    return self.send({"error": "Invalid profile ID."}, 400)
                with storage.connect() as con:
                    row = con.execute(
                        "SELECT name FROM people WHERE person_id=? AND deleted_at IS NOT NULL",
                        (person_id,),
                    ).fetchone()
                    if not row:
                        return self.send(
                            {"error": "Deleted profile was not found."}, 404
                        )
                    con.execute(
                        "UPDATE people SET deleted_at=NULL WHERE person_id=?",
                        (person_id,),
                    )
                MODEL_PATH.unlink(missing_ok=True)
                LABELS_PATH.unlink(missing_ok=True)
                storage.ensure_today_rows()
                storage.refresh_exports()
                started = _start_training()
                msg = f"{row[0]} restored. Existing face samples and attendance history are back."
                if started:
                    msg += " The recognition model is updating automatically."
                elif len(storage.list_people()) < 2:
                    msg += " Recognition will become available after one more person is registered or restored."
                return self.send({"ok": True, "message": msg})
            if action == "permanently_delete_person":
                if _state.get("scan"):
                    return self.send(
                        {
                            "error": "Stop the active camera scan before permanently deleting a profile."
                        },
                        409,
                    )
                person_id = str(data.get("person_id", ""))
                if not re.fullmatch(r"[a-f0-9]{32}", person_id):
                    return self.send({"error": "Invalid profile ID."}, 400)
                with storage.connect() as con:
                    row = con.execute(
                        "SELECT name FROM people WHERE person_id=? AND deleted_at IS NOT NULL",
                        (person_id,),
                    ).fetchone()
                    if not row:
                        return self.send(
                            {"error": "Deleted profile was not found."}, 404
                        )
                    con.execute(
                        "DELETE FROM attendance WHERE person_id=?", (person_id,)
                    )
                    con.execute(
                        "DELETE FROM profile_details WHERE person_id=?", (person_id,)
                    )
                    con.execute("DELETE FROM people WHERE person_id=?", (person_id,))
                shutil.rmtree(FACES_DIR / person_id, ignore_errors=True)
                MODEL_PATH.unlink(missing_ok=True)
                LABELS_PATH.unlink(missing_ok=True)
                storage.refresh_exports()
                started = _start_training()
                msg = f"{row[0]} and their face samples/attendance history were permanently deleted."
                if started:
                    msg += " The recognition model is updating automatically."
                elif len(storage.list_people()) < 2:
                    msg += (
                        " Register or restore another person before using recognition."
                    )
                return self.send({"ok": True, "message": msg})
            if action in ("attendance", "exit"):
                if _registration_active():
                    return self.send(
                        {"error": "Face registration is in progress. Wait for it to finish before starting a scan."},
                        409,
                    )
                if _state["scan"]:
                    return self.send(
                        {"error": "A camera scan is already running."}, 409
                    )
                if _state["training"]:
                    return self.send(
                        {
                            "error": "The recognition model is updating. Wait until the update finishes, then start the scan."
                        },
                        409,
                    )
                if not _model_is_current():
                    return self.send(
                        {
                            "error": "Register at least two people. The recognition model will update automatically."
                        },
                        400,
                    )
                stop = threading.Event()
                _state.update(
                    scan=action,
                    stop=stop,
                    error=None,
                    scan_status=f"Connecting to {data.get('camera', 'System camera')}…",
                )

                def work():
                    try:
                        def report_scan(message):
                            _state["scan_status"] = message

                        scan(
                            action,
                            data.get("camera", "System camera"),
                            str(data.get("source", data.get("camera_index", 0))),
                            stop,
                            report_scan,
                            None,
                        )
                    except Exception as exc:
                        _state["error"] = str(exc)
                    finally:
                        _state.update(
                            scan=None,
                            stop=None,
                            scan_status="Camera scan stopped.",
                        )

                threading.Thread(target=work, daemon=True).start()
                return self.send(
                    {
                        "ok": True,
                        "message": f"{action.title()} camera started. Press Q in the camera window to stop.",
                    }
                )
            if action == "stop":
                if _state["stop"]:
                    _state["stop"].set()
                return self.send({"ok": True, "message": "Stopping scan."})
            return self.send({"error": "Unknown action."}, 400)
        except Exception as e:
            return self.send({"error": str(e)}, 500)


def main():
    storage.initialize()
    if not _model_is_current():
        _start_training()
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:8765")).start()
    print("CampusFlow is running at http://127.0.0.1:8765 — close this window to stop.")
    server.serve_forever()
