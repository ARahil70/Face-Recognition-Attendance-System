"""SQLite records and CSV reports for CampusFlow."""

import csv
import sqlite3
from datetime import datetime

from .config import BASE_DIR, DATA_DIR, DB_PATH

STUDENT_CSV = BASE_DIR / "student_attendance.csv"
FACULTY_CSV = BASE_DIR / "faculty_attendance.csv"
STUDENT_EXIT_CSV = BASE_DIR / "student_exit.csv"
FACULTY_EXIT_CSV = BASE_DIR / "faculty_exit.csv"
EXIT_CSV = BASE_DIR / "exit_log.csv"
ROSTER_CSV = BASE_DIR / "registered_people.csv"


def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=20)
    con.execute("PRAGMA journal_mode=WAL")
    return con


def initialize():
    with connect() as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS people(
            person_id TEXT PRIMARY KEY,name TEXT NOT NULL,role TEXT NOT NULL,
            created_at TEXT NOT NULL,deleted_at TEXT,UNIQUE(name,role))"""
        )
        con.execute(
            """CREATE TABLE IF NOT EXISTS attendance(
            day TEXT NOT NULL,person_id TEXT NOT NULL,name TEXT NOT NULL,role TEXT NOT NULL,
            first_seen TEXT NOT NULL DEFAULT '',PRIMARY KEY(day,person_id))"""
        )
        con.execute(
            """CREATE TABLE IF NOT EXISTS profile_details(
            person_id TEXT PRIMARY KEY,institution TEXT NOT NULL DEFAULT 'Mewar University',
            course TEXT NOT NULL DEFAULT '',branch TEXT NOT NULL DEFAULT '',section TEXT NOT NULL DEFAULT '',
            FOREIGN KEY(person_id) REFERENCES people(person_id))"""
        )
        cols = {r[1] for r in con.execute("PRAGMA table_info(attendance)")}
        if "status" not in cols:
            con.execute(
                "ALTER TABLE attendance ADD COLUMN status TEXT NOT NULL DEFAULT 'P'"
            )
        if "exit_time" not in cols:
            con.execute("ALTER TABLE attendance ADD COLUMN exit_time TEXT")
        people_cols = {r[1] for r in con.execute("PRAGMA table_info(people)")}
        if "deleted_at" not in people_cols:
            con.execute("ALTER TABLE people ADD COLUMN deleted_at TEXT")
    ensure_today_rows()
    refresh_exports()


def ensure_today_rows(day=None):
    day = day or datetime.now().strftime("%Y-%m-%d")
    with connect() as con:
        people = con.execute(
            "SELECT person_id,name,role FROM people WHERE deleted_at IS NULL"
        ).fetchall()
        con.executemany(
            "INSERT OR IGNORE INTO attendance(day,person_id,name,role,first_seen,status,exit_time) VALUES(?,?,?,?,?,'A',NULL)",
            [(day, *person, "") for person in people],
        )


def register_person(person_id, name, role, details=None):
    with connect() as con:
        con.execute(
            "INSERT INTO people(person_id,name,role,created_at) VALUES(?,?,?,?)",
            (person_id, name, role, datetime.now().isoformat(timespec="seconds")),
        )
        con.execute(
            "INSERT OR IGNORE INTO attendance(day,person_id,name,role,first_seen,status) VALUES(?,?,?,?,?,'A')",
            (datetime.now().strftime("%Y-%m-%d"), person_id, name, role, ""),
        )
        details = details or {}
        con.execute(
            "INSERT OR REPLACE INTO profile_details(person_id,institution,course,branch,section) VALUES(?,?,?,?,?)",
            (
                person_id,
                details.get("institution", "Mewar University"),
                details.get("course", ""),
                details.get("branch", ""),
                details.get("section", ""),
            ),
        )
    refresh_exports()


def list_people(role=None):
    with connect() as con:
        if role in ("Student", "Faculty"):
            return con.execute(
                "SELECT person_id,name,role FROM people WHERE deleted_at IS NULL AND role=? ORDER BY name COLLATE NOCASE",
                (role,),
            ).fetchall()
        return con.execute(
            "SELECT person_id,name,role FROM people WHERE deleted_at IS NULL ORDER BY role,name COLLATE NOCASE"
        ).fetchall()


def list_deleted_people():
    with connect() as con:
        return con.execute(
            """SELECT p.person_id,p.name,p.role,p.created_at,p.deleted_at,
            COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'')
            FROM people p LEFT JOIN profile_details d USING(person_id)
            WHERE p.deleted_at IS NOT NULL ORDER BY p.deleted_at DESC,p.name COLLATE NOCASE"""
        ).fetchall()


def _write(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def refresh_exports():
    with connect() as con:
        roster = con.execute(
            "SELECT p.person_id,p.name,p.role,p.created_at,COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'') FROM people p LEFT JOIN profile_details d USING(person_id) WHERE p.deleted_at IS NULL ORDER BY p.role,p.name COLLATE NOCASE"
        ).fetchall()
        rows = con.execute(
            "SELECT a.day,a.name,a.role,a.status,a.first_seen,COALESCE(a.exit_time,''),COALESCE(d.course,''),COALESCE(d.branch,''),COALESCE(d.section,'') FROM attendance a LEFT JOIN profile_details d USING(person_id) ORDER BY a.day,a.name COLLATE NOCASE"
        ).fetchall()
    _write(
        ROSTER_CSV,
        ["Person ID", "Name", "Role", "Registered At", "Course", "Branch", "Section"],
        roster,
    )
    for role, path in (("Student", STUDENT_CSV), ("Faculty", FACULTY_CSV)):
        _write(
            path,
            [
                "Date",
                "Name",
                "Status (P/A)",
                "Entry Time",
                "Course",
                "Branch",
                "Section",
            ],
            [
                (day, name, status, entry, course, branch, section)
                for day, name, r, status, entry, exit_time, course, branch, section in rows
                if r == role
            ],
        )
    exits = [
        (day, name, role, exit_time, course, branch, section)
        for day, name, role, status, entry, exit_time, course, branch, section in rows
        if exit_time
    ]
    _write(
        EXIT_CSV,
        ["Date", "Name", "Role", "Exit Time", "Course", "Branch", "Section"],
        exits,
    )
    for role, path in (("Student", STUDENT_EXIT_CSV), ("Faculty", FACULTY_EXIT_CSV)):
        _write(
            path,
            ["Date", "Name", "Exit Time", "Course", "Branch", "Section"],
            [
                (day, name, exit_time, course, branch, section)
                for day, name, r, exit_time, course, branch, section in exits
                if r == role
            ],
        )


def mark(person_id, mode):
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    tm = now.strftime("%H:%M:%S")
    ensure_today_rows(day)
    with connect() as con:
        if not con.execute(
            "SELECT 1 FROM people WHERE person_id=? AND deleted_at IS NULL",
            (person_id,),
        ).fetchone():
            return False, "This profile is in the Recycle Bin."
        row = con.execute(
            "SELECT status,first_seen,exit_time FROM attendance WHERE day=? AND person_id=?",
            (day, person_id),
        ).fetchone()
        if not row:
            return False, "Unknown person."
        if mode == "attendance":
            if row[0] == "P":
                return False, "Already present today."
            con.execute(
                "UPDATE attendance SET status='P',first_seen=? WHERE day=? AND person_id=?",
                (tm, day, person_id),
            )
            message = "Present marked."
        else:
            if row[0] != "P":
                return False, "Attendance not marked; exit not recorded."
            if row[2]:
                return False, "Exit already recorded today."
            con.execute(
                "UPDATE attendance SET exit_time=? WHERE day=? AND person_id=?",
                (tm, day, person_id),
            )
            message = "Exit recorded."
    refresh_exports()
    return True, message


def today_records(role=None):
    day = datetime.now().strftime("%Y-%m-%d")
    ensure_today_rows(day)
    with connect() as con:
        query = "SELECT a.name,a.role,a.status,a.first_seen,COALESCE(a.exit_time,'') FROM attendance a JOIN people p USING(person_id) WHERE a.day=? AND p.deleted_at IS NULL"
        args = [day]
        if role in ("Student", "Faculty"):
            query += " AND a.role=?"
            args.append(role)
        query += " ORDER BY a.role,a.name COLLATE NOCASE"
        return con.execute(query, args).fetchall()


def today_stats(role=None):
    rows = today_records(role)
    return {
        "total": len(rows),
        "present": sum(r[2] == "P" for r in rows),
        "absent": sum(r[2] == "A" for r in rows),
        "exited": sum(bool(r[4]) for r in rows),
    }
