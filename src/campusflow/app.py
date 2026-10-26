"""CampusFlow desktop dashboard."""

import json
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from .camera import capture, discard_samples
from .config import BASE_DIR, LABELS_PATH, MODEL_PATH
from .recognition import duplicate_face, scan, train
from .storage import (
    FACULTY_CSV,
    FACULTY_EXIT_CSV,
    ROSTER_CSV,
    STUDENT_CSV,
    STUDENT_EXIT_CSV,
    initialize,
    list_people,
    register_person,
    today_records,
    today_stats,
)

NAVY = "#17263C"
NAVY2 = "#213650"
CANVAS = "#F3F6FA"
WHITE = "#FFFFFF"
TEXT = "#1B2A41"
MUTED = "#75849A"
TEAL = "#16AFA0"
BLUE = "#4778F5"
GREEN = "#159B73"
RED = "#DE5B67"
AMBER = "#E6A23C"
BORDER = "#E7ECF2"
SETTINGS = BASE_DIR / "data" / "app_settings.json"


class RoundedCard(tk.Frame):
    def __init__(self, parent, bg=WHITE, radius=18, **kwargs):
        super().__init__(parent, bg=parent.cget("bg"), **kwargs)
        self.radius = radius
        self.bg = bg
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            borderwidth=0,
            bg=parent.cget("bg"),
            width=320,
            height=120,
        )
        self.canvas.pack(fill="both", expand=True)
        self.body = tk.Frame(self.canvas, bg=bg)
        self.window = self.canvas.create_window(14, 14, anchor="nw", window=self.body)
        self.canvas.bind("<Configure>", self._paint)

    def _poly(self, x1, y1, x2, y2, r):
        return [
            x1 + r,
            y1,
            x2 - r,
            y1,
            x2,
            y1 + r,
            x2,
            y2 - r,
            x2 - r,
            y2,
            x1 + r,
            y2,
            x1,
            y2 - r,
            x1,
            y1 + r,
        ]

    def _paint(self, event):
        c = self.canvas
        c.delete("shape")
        w = max(40, event.width)
        h = max(40, event.height)
        r = min(self.radius, w / 5, h / 5)
        c.create_polygon(
            *self._poly(5, 7, w - 3, h - 3, r),
            smooth=True,
            splinesteps=24,
            fill="#E2E8F0",
            outline="",
            tags="shape",
        )
        c.create_polygon(
            *self._poly(3, 2, w - 5, h - 8, r),
            smooth=True,
            splinesteps=24,
            fill=self.bg,
            outline=BORDER,
            tags="shape",
        )
        c.coords(self.window, 14, 12)
        c.itemconfigure(self.window, width=max(10, w - 30), height=max(10, h - 27))
        c.tag_lower("shape")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusFlow | Smart Attendance")
        self.root.geometry("1320x820")
        self.root.minsize(1080, 700)
        self.root.configure(bg=CANVAS)
        self.job = False
        self.stop = threading.Event()
        self.scanning = False
        self.page = "Overview"
        self.role_filter = "Student"
        self.status_filter = "All"
        self.preview = None
        self.preview_photo = None
        self.last_preview_update = 0
        initialize()
        self.settings = self._load_settings()
        self._style()
        self._layout()
        self.show_page("Overview")
        root.after(1600, self.autostart)

    def _load_settings(self):
        try:
            return json.loads(SETTINGS.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_setting(self, mode, kind, source):
        self.settings[mode] = {"kind": kind, "source": source}
        SETTINGS.parent.mkdir(exist_ok=True)
        SETTINGS.write_text(json.dumps(self.settings, indent=2), encoding="utf-8")

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure(
            "Treeview",
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT,
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        s.configure(
            "Treeview.Heading",
            background="#F5F7FA",
            foreground=MUTED,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )
        s.map(
            "Treeview",
            background=[("selected", "#D8F3EF")],
            foreground=[("selected", TEXT)],
        )
        s.configure(
            "TCombobox",
            padding=8,
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
        )

    def _layout(self):
        shell = tk.Frame(self.root, bg=CANVAS)
        shell.pack(fill="both", expand=True)
        self.sidebar = tk.Frame(shell, bg=NAVY, width=236)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        brand = tk.Frame(self.sidebar, bg=NAVY)
        brand.pack(fill="x", padx=22, pady=(25, 30))
        mark = tk.Label(
            brand,
            text="CF",
            font=("Segoe UI", 13, "bold"),
            bg=TEAL,
            fg=WHITE,
            width=3,
            height=1,
        )
        mark.pack(side="left", ipady=5)
        texts = tk.Frame(brand, bg=NAVY)
        texts.pack(side="left", padx=10)
        tk.Label(
            texts, text="CampusFlow", font=("Segoe UI", 15, "bold"), bg=NAVY, fg=WHITE
        ).pack(anchor="w")
        tk.Label(
            texts,
            text="SMART ATTENDANCE",
            font=("Segoe UI", 8, "bold"),
            bg=NAVY,
            fg="#8FA2BA",
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            font=("Segoe UI", 8, "bold"),
            bg=NAVY,
            fg="#8294AA",
        ).pack(anchor="w", padx=24, pady=(0, 8))
        self.nav_buttons = {}
        for title, label in [
            ("Overview", "Overview"),
            ("Register person", "Register"),
            ("Attendance", "Attendance"),
            ("Exit records", "Exit records"),
            ("People", "People"),
        ]:
            b = tk.Button(
                self.sidebar,
                text="  " + label,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=12,
                pady=11,
                bg=NAVY,
                fg="#D1DCE8",
                activebackground=NAVY2,
                activeforeground=WHITE,
                command=lambda p=title: self.show_page(p),
            )
            b.pack(fill="x", padx=14, pady=3)
            self.nav_buttons[title] = b
        bottom = tk.Frame(self.sidebar, bg=NAVY)
        bottom.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Frame(bottom, bg="#2D4058", height=1).pack(fill="x", pady=(0, 12))
        tk.Label(
            bottom,
            text="CAMERA STATUS",
            font=("Segoe UI", 8, "bold"),
            bg=NAVY,
            fg="#8294AA",
        ).pack(anchor="w")
        self.side_status = tk.Label(
            bottom, text="● Ready", font=("Segoe UI", 10), bg=NAVY, fg="#58D2B0"
        )
        self.side_status.pack(anchor="w", pady=(4, 0))
        self.main = tk.Frame(shell, bg=CANVAS)
        self.main.pack(side="left", fill="both", expand=True)
        self.header = tk.Frame(self.main, bg=CANVAS)
        self.header.pack(fill="x", padx=30, pady=(22, 8))
        self.heading = tk.Label(
            self.header, text="", font=("Segoe UI", 22, "bold"), bg=CANVAS, fg=TEXT
        )
        self.heading.pack(side="left")
        self.date_label = tk.Label(
            self.header,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Segoe UI", 10),
            bg=CANVAS,
            fg=MUTED,
        )
        self.date_label.pack(side="right", pady=8)
        self.subtitle = tk.Label(
            self.main, text="", font=("Segoe UI", 10), bg=CANVAS, fg=MUTED
        )
        self.subtitle.pack(anchor="w", padx=32, pady=(0, 8))
        self.content = tk.Frame(self.main, bg=CANVAS)
        self.content.pack(fill="both", expand=True, padx=24, pady=(2, 8))
        self.statusbar = tk.Label(
            self.main,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 9),
            bg="#E9EEF4",
            fg="#53657B",
            padx=14,
            pady=8,
        )
        self.statusbar.pack(fill="x", side="bottom")

    def _button(self, parent, text, command, color=TEAL, fg=WHITE):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            bg=color,
            fg=fg,
            activebackground=color,
            activeforeground=fg,
            padx=15,
            pady=9,
        )

    def _card(self, parent, **kw):
        return RoundedCard(parent, **kw)

    def _role_picker(self, parent, all_option=False):
        box = tk.Frame(parent, bg=CANVAS)
        box.pack(anchor="w", pady=(0, 12))
        roles = ["Student", "Faculty"] + (["Both"] if all_option else [])
        for role in roles:
            active = self.role_filter == role
            tk.Button(
                box,
                text=role,
                command=lambda r=role: self._set_role(r),
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                bg=TEAL if active else WHITE,
                fg=WHITE if active else MUTED,
                padx=16,
                pady=7,
            ).pack(side="left", padx=(0, 6))

    def _set_role(self, role):
        self.role_filter = role
        self.show_page(self.page)

    def show_page(self, page):
        self.page = page
        for key, b in self.nav_buttons.items():
            b.configure(
                bg=NAVY2 if key == page else NAVY,
                fg=WHITE if key == page else "#D1DCE8",
            )
        titles = {
            "Overview": ("Good day", "Here is today’s attendance at a glance."),
            "Register": (
                "Register a person",
                "Create a secure face profile for a student or faculty member.",
            ),
            "Attendance": (
                "Attendance",
                "Review today’s presence and run the recognition camera.",
            ),
            "Exit records": (
                "Exit records",
                "Record and review departure times separately by role.",
            ),
            "People": (
                "People directory",
                "Registered profiles and their current status.",
            ),
        }
        self.heading.configure(text=titles[page][0])
        self.subtitle.configure(text=titles[page][1])
        for child in self.content.winfo_children():
            child.destroy()
        self.preview = None
        {
            "Overview": self._overview,
            "Register": self._register,
            "Attendance": self._attendance,
            "Exit records": self._exits,
            "People": self._people,
        }[page]()

    def _summary_card(self, parent, title, value, caption, color):
        card = self._card(parent)
        card.pack(side="left", fill="both", expand=True, padx=(0, 12))
        body = card.body
        tk.Label(
            body, text=title.upper(), font=("Segoe UI", 8, "bold"), bg=WHITE, fg=MUTED
        ).pack(anchor="w", padx=16, pady=(14, 2))
        tk.Label(
            body, text=str(value), font=("Segoe UI", 25, "bold"), bg=WHITE, fg=color
        ).pack(anchor="w", padx=16)
        tk.Label(body, text=caption, font=("Segoe UI", 9), bg=WHITE, fg=MUTED).pack(
            anchor="w", padx=16, pady=(0, 13)
        )

    def _table(self, parent, columns, rows, height=9):
        frame = tk.Frame(parent, bg=WHITE)
        frame.pack(fill="both", expand=True, padx=14, pady=(6, 14))
        tree = ttk.Treeview(
            frame, columns=[c[0] for c in columns], show="headings", height=height
        )
        for key, label, width in columns:
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor="w")
        tree.tag_configure("present", foreground=GREEN)
        tree.tag_configure("absent", foreground=RED)
        tree.tag_configure("exit", foreground=BLUE)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        for values in rows:
            tag = (
                "present" if "P" in values else ("absent" if "A" in values else "exit")
            )
            tree.insert("", "end", values=values, tags=(tag,))
        return tree

    def _overview(self):
        self._role_picker(self.content, all_option=True)
        stats = today_stats(None if self.role_filter == "Both" else self.role_filter)
        row = tk.Frame(self.content, bg=CANVAS)
        row.pack(fill="x", pady=(0, 12))
        self._summary_card(row, "Registered", stats["total"], "In selected group", BLUE)
        self._summary_card(row, "Present", stats["present"], "Marked today", GREEN)
        self._summary_card(row, "Absent", stats["absent"], "Not seen today", RED)
        self._summary_card(row, "Exited", stats["exited"], "Exit recorded", AMBER)
        lower = tk.Frame(self.content, bg=CANVAS)
        lower.pack(fill="both", expand=True)
        left = self._card(lower)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = self._card(lower)
        right.pack(side="left", fill="both", expand=True)
        tk.Label(
            left.body,
            text="Today’s attendance",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=16, pady=(15, 3))
        filterbar = tk.Frame(left.body, bg=WHITE)
        filterbar.pack(fill="x", padx=14)
        for label in ("All", "Present", "Absent"):
            tk.Button(
                filterbar,
                text=label,
                command=lambda x=label: self._filter_status(x),
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                bd=0,
                bg=TEAL if self.status_filter == label else "#F1F4F8",
                fg=WHITE if self.status_filter == label else MUTED,
                padx=10,
                pady=5,
            ).pack(side="left", padx=(0, 5), pady=4)
        rows = today_records(None if self.role_filter == "Both" else self.role_filter)
        values = [
            (n, r, s or "A", entry or "—", exit_time or "—")
            for n, r, s, entry, exit_time in rows
            if self.status_filter == "All"
            or (self.status_filter == "Present" and s == "P")
            or (self.status_filter == "Absent" and s == "A")
        ]
        self._table(
            left.body,
            [
                ("name", "NAME", 160),
                ("role", "ROLE", 80),
                ("status", "STATUS", 70),
                ("entry", "ENTRY", 90),
                ("exit", "EXIT", 90),
            ],
            values,
            8,
        )
        tk.Label(
            right.body,
            text="Live camera",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=16, pady=(15, 4))
        self._preview(right.body)
        rowb = tk.Frame(right.body, bg=WHITE)
        rowb.pack(fill="x", padx=14, pady=(4, 14))
        self._button(
            rowb,
            "Start attendance",
            lambda: self._start_from("attendance", "Both"),
            BLUE,
        ).pack(side="left", padx=(0, 6))
        self._button(rowb, "Stop camera", self.stop_scan, "#EAF0F6", TEXT).pack(
            side="left"
        )

    def _filter_status(self, value):
        self.status_filter = value
        self.show_page(self.page)

    def _preview(self, parent):
        box = tk.Frame(parent, bg="#E9EFF5", height=205)
        box.pack(fill="both", expand=True, padx=14, pady=8)
        box.pack_propagate(False)
        self.preview = tk.Label(
            box,
            text="Camera preview\nStart a scan to view live recognition",
            font=("Segoe UI", 10),
            bg="#E9EFF5",
            fg=MUTED,
            justify="center",
        )
        self.preview.pack(fill="both", expand=True)

    def _show_frame(self, frame):
        if time.monotonic() - self.last_preview_update < 0.12:
            return
        self.last_preview_update = time.monotonic()

        def update():
            if self.preview is None or not self.preview.winfo_exists():
                return
            rgb = Image.fromarray(frame[:, :, ::-1].copy())
            rgb.thumbnail((520, 240))
            self.preview_photo = ImageTk.PhotoImage(rgb)
            self.preview.configure(image=self.preview_photo, text="")

        self.root.after(0, update)

    def _register(self):
        grid = tk.Frame(self.content, bg=CANVAS)
        grid.pack(fill="both", expand=True)
        form = self._card(grid)
        form.pack(side="left", fill="both", expand=True, padx=(0, 12))
        side = self._card(grid)
        side.pack(side="left", fill="both", expand=True)
        body = form.body
        tk.Label(
            body,
            text="New face profile",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=20, pady=(18, 3))
        tk.Label(
            body,
            text="Duplicate name/role and strong matches to an enrolled face are rejected.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED,
            wraplength=470,
        ).pack(anchor="w", padx=20, pady=(0, 10))
        self.name = tk.StringVar()
        self.reg_role = tk.StringVar(value="Student")
        self.reg_kind = tk.StringVar(value="System camera")
        self.reg_source = tk.StringVar(value="0")
        self._field(
            body,
            "Full name",
            tk.Entry(
                body,
                textvariable=self.name,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
            ),
        )
        self._field(
            body,
            "Profile type",
            ttk.Combobox(
                body,
                textvariable=self.reg_role,
                values=["Student", "Faculty"],
                state="readonly",
            ),
        )
        self._field(
            body,
            "Camera source",
            ttk.Combobox(
                body,
                textvariable=self.reg_kind,
                values=["System camera", "IP Webcam"],
                state="readonly",
            ),
        )
        self._field(
            body,
            "Camera index / IP URL",
            tk.Entry(
                body,
                textvariable=self.reg_source,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
            ),
        )
        tk.Label(
            body,
            text="System camera index is usually 0. For phone, choose IP Webcam and enter its shot.jpg URL.",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED,
            wraplength=470,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(3, 9))
        self._button(body, "Capture and register", self.enroll, TEAL).pack(
            anchor="w", padx=20, pady=(3, 15)
        )
        self._button(body, "Retrain recognition model", self.train_now, BLUE).pack(
            anchor="w", padx=20, pady=(0, 12)
        )
        info = tk.Frame(body, bg="#EFF8F6")
        info.pack(fill="x", padx=20, pady=(0, 18))
        tk.Label(
            info,
            text="Guided capture • 100 sharp frames • 5 gentle face angles • roughly 45 seconds",
            font=("Segoe UI", 9, "bold"),
            bg="#EFF8F6",
            fg="#267C72",
            wraplength=480,
            justify="left",
        ).pack(anchor="w", padx=12, pady=12)
        tk.Label(
            side.body,
            text="Registered people",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=18, pady=(18, 4))
        people = list_people()
        tk.Label(
            side.body,
            text=f"{len(people)} profiles • Student and Faculty roles",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED,
        ).pack(anchor="w", padx=18, pady=(0, 5))
        rows = [(name, role) for pid, name, role in people]
        self._table(side.body, [("name", "NAME", 230), ("role", "ROLE", 100)], rows, 12)

    def _field(self, parent, label, widget):
        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill="x", padx=20, pady=6)
        tk.Label(
            row,
            text=label,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg="#53657B",
            width=22,
            anchor="w",
        ).pack(side="left")
        widget.pack(side="left", fill="x", expand=True, ipady=7)

    def _camera_controls(self, parent, mode, role):
        saved = self.settings.get(mode, {})
        kind = tk.StringVar(value=saved.get("kind", "System camera"))
        source = tk.StringVar(value=saved.get("source", "0"))
        c = self._card(parent)
        c.pack(fill="x", pady=(0, 12))
        b = c.body
        tk.Label(
            b, text="Camera setup", font=("Segoe UI", 12, "bold"), bg=WHITE, fg=TEXT
        ).pack(anchor="w", padx=14, pady=(12, 4))
        row = tk.Frame(b, bg=WHITE)
        row.pack(fill="x", padx=12, pady=(0, 10))
        ttk.Combobox(
            row,
            textvariable=kind,
            values=["System camera", "IP Webcam"],
            state="readonly",
            width=18,
        ).pack(side="left", padx=4)
        tk.Entry(
            row,
            textvariable=source,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=35,
        ).pack(side="left", padx=4, ipady=6)
        self._button(
            row,
            "Start scan",
            lambda: self._start_from(mode, role, kind, source),
            TEAL if mode == "attendance" else BLUE,
        ).pack(side="left", padx=4)
        self._button(row, "Stop", self.stop_scan, "#EDF1F6", TEXT).pack(
            side="left", padx=4
        )
        return kind, source

    def _attendance(self):
        self._role_picker(self.content, all_option=True)
        stats = today_stats(None if self.role_filter == "Both" else self.role_filter)
        row = tk.Frame(self.content, bg=CANVAS)
        row.pack(fill="x", pady=(0, 10))
        for title, key, color in [
            ("Present", "present", GREEN),
            ("Absent", "absent", RED),
            ("Registered", "total", BLUE),
        ]:
            self._summary_card(row, title, stats[key], "Today", color)
        lower = tk.Frame(self.content, bg=CANVAS)
        lower.pack(fill="both", expand=True)
        left = tk.Frame(lower, bg=CANVAS)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = self._card(lower)
        right.pack(side="left", fill="both", expand=True)
        self._camera_controls(left, "attendance", self.role_filter)
        tk.Label(
            left,
            text="Present and absent list",
            font=("Segoe UI", 13, "bold"),
            bg=CANVAS,
            fg=TEXT,
        ).pack(anchor="w", pady=(2, 4))
        filterbar = tk.Frame(left, bg=CANVAS)
        filterbar.pack(anchor="w", pady=(0, 4))
        for val in ("All", "Present", "Absent"):
            tk.Button(
                filterbar,
                text=val,
                command=lambda v=val: self._filter_status(v),
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                bd=0,
                bg=TEAL if self.status_filter == val else WHITE,
                fg=WHITE if self.status_filter == val else MUTED,
                padx=10,
                pady=5,
            ).pack(side="left", padx=(0, 5))
        records = today_records(
            None if self.role_filter == "Both" else self.role_filter
        )
        rows = [
            (n, r, s, e or "—")
            for n, r, s, e, x in records
            if self.status_filter == "All"
            or (self.status_filter == "Present" and s == "P")
            or (self.status_filter == "Absent" and s == "A")
        ]
        card = self._card(left)
        card.pack(fill="both", expand=True)
        self._table(
            card.body,
            [
                ("name", "NAME", 180),
                ("role", "ROLE", 85),
                ("status", "STATUS", 80),
                ("entry", "ENTRY", 100),
            ],
            rows,
            8,
        )
        tk.Label(
            right.body,
            text="Live recognition",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=14, pady=(14, 5))
        self._preview(right.body)
        self._button(
            right.body,
            "Open attendance report",
            lambda: self._open(
                STUDENT_CSV if self.role_filter == "Student" else FACULTY_CSV
            ),
            BLUE,
        ).pack(anchor="w", padx=14, pady=8)

    def _exits(self):
        self._role_picker(self.content)
        stats = today_stats(self.role_filter)
        row = tk.Frame(self.content, bg=CANVAS)
        row.pack(fill="x", pady=(0, 10))
        self._summary_card(row, "Present", stats["present"], "Today", GREEN)
        self._summary_card(row, "Exit recorded", stats["exited"], "Today", BLUE)
        self._summary_card(
            row,
            "Still on campus",
            max(0, stats["present"] - stats["exited"]),
            "Not checked out",
            AMBER,
        )
        lower = tk.Frame(self.content, bg=CANVAS)
        lower.pack(fill="both", expand=True)
        left = tk.Frame(lower, bg=CANVAS)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = self._card(lower)
        right.pack(side="left", fill="both", expand=True)
        self._camera_controls(left, "exit", self.role_filter)
        tk.Label(
            left,
            text=f"{self.role_filter} exit report",
            font=("Segoe UI", 13, "bold"),
            bg=CANVAS,
            fg=TEXT,
        ).pack(anchor="w", pady=5)
        records = today_records(self.role_filter)
        rows = [(n, r, x) for n, r, s, e, x in records if x]
        card = self._card(left)
        card.pack(fill="both", expand=True)
        self._table(
            card.body,
            [("name", "NAME", 190), ("role", "ROLE", 100), ("exit", "EXIT TIME", 120)],
            rows,
            8,
        )
        tk.Label(
            right.body,
            text="Exit camera preview",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=14, pady=(14, 5))
        self._preview(right.body)
        path = STUDENT_EXIT_CSV if self.role_filter == "Student" else FACULTY_EXIT_CSV
        self._button(
            right.body, "Open exit report", lambda: self._open(path), BLUE
        ).pack(anchor="w", padx=14, pady=8)

    def _people(self):
        row = tk.Frame(self.content, bg=CANVAS)
        row.pack(fill="x", pady=(0, 10))
        self._role_picker(row, all_option=True)
        role = None if self.role_filter == "Both" else self.role_filter
        people = list_people(role)
        card = self._card(self.content)
        card.pack(fill="both", expand=True)
        tk.Label(
            card.body,
            text=f"{len(people)} registered profiles",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=TEXT,
        ).pack(anchor="w", padx=15, pady=(14, 2))
        self._table(
            card.body,
            [("name", "NAME", 260), ("role", "ROLE", 100)],
            [(n, r) for pid, n, r in people],
            16,
        )
        self._button(
            card.body, "Open roster file", lambda: self._open(ROSTER_CSV), BLUE
        ).pack(anchor="w", padx=14, pady=(0, 12))

    def _open(self, path):
        try:
            if not path.exists():
                raise FileNotFoundError(path)
            import os

            os.startfile(str(path))
        except Exception as e:
            messagebox.showerror("Could not open file", str(e))

    def status(self, msg):
        def update():
            self.statusbar.configure(text=msg)
            self.side_status.configure(
                text="● Scanning" if self.scanning else "● Ready",
                fg=TEAL if self.scanning else "#58D2B0",
            )

        self.root.after(0, update)

    def enroll(self):
        if self.job or self.scanning:
            messagebox.showinfo(
                "Camera in use",
                "Stop the current scan before registering a new person.",
            )
            return
        name = self.name.get().strip()
        role = self.reg_role.get()
        if not name:
            messagebox.showwarning("Name required", "Enter the person’s full name.")
            return
        if any(
            n.casefold() == name.casefold() and r == role for _, n, r in list_people()
        ):
            messagebox.showwarning(
                "Already registered", f"{name} is already registered as {role}."
            )
            return
        kind = self.reg_kind.get()
        source = self.reg_source.get()
        self.job = True

        def work():
            try:
                pid = capture(name, role, kind, source, self.status)
                duplicate = duplicate_face(pid)
                if duplicate:
                    discard_samples(pid)
                    raise RuntimeError(
                        f"This face strongly matches {duplicate['name']} ({duplicate['role']}). No second profile was saved."
                    )
                register_person(pid, name, role)
                people = len(list_people())
                self.status(
                    f"{name} registered. Face images saved in data/faces/{pid}."
                )
                if people >= 2:
                    self.status("Registration complete. Updating recognition model…")
                    count = train(self.status)
                    self.status(
                        f"Model updated for {count} people. Starting attendance scan."
                    )
                    self.root.after(400, self.autostart)
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Registration complete",
                        f"{name} ({role}) has been registered.\n100 clear samples were saved.",
                    ),
                )
                self.root.after(100, self.show_page, "People")
            except Exception as e:
                self.status(f"Registration rejected: {e}")
                self.root.after(
                    0,
                    lambda msg=str(e): messagebox.showerror(
                        "Please capture again", msg
                    ),
                )
            finally:
                self.job = False

        threading.Thread(target=work, daemon=True).start()

    def _start_from(self, mode, role, kind=None, source=None):
        if kind is None:
            saved = self.settings.get(mode, {})
            kind_value = saved.get("kind", "System camera")
            source_value = saved.get("source", "0")
        else:
            kind_value = kind.get()
            source_value = source.get()
        self.start_scan(mode, kind_value, source_value, role)

    def train_now(self):
        if self.job or self.scanning:
            messagebox.showinfo(
                "Camera in use", "Stop the active scan before retraining."
            )
            return
        self.job = True

        def work():
            try:
                count = train(self.status)
                self.status(f"Recognition model updated for {count} people.")
                self.root.after(400, self.autostart)
            except Exception as e:
                self.root.after(
                    0,
                    lambda msg=str(e): messagebox.showerror(
                        "Could not train model", msg
                    ),
                )
                self.status(f"Model update failed: {e}")
            finally:
                self.job = False

        threading.Thread(target=work, daemon=True).start()

    def start_scan(self, mode, kind, source, role):
        if self.scanning or self.job:
            messagebox.showinfo(
                "Busy", "Stop the current scan or wait for registration to finish."
            )
            return
        if not MODEL_PATH.exists() or not LABELS_PATH.exists():
            messagebox.showwarning(
                "Model needed", "Register two people and train the face model first."
            )
            return
        self._save_setting(mode, kind, source)
        self.stop.clear()
        self.scanning = True
        self.status(f"{mode.title()} scan active • {role}")
        self.side_status.configure(text="● Scanning", fg=TEAL)

        def work():
            try:
                scan(
                    mode,
                    kind,
                    source,
                    self.stop,
                    self.status,
                    None if role == "Both" else role,
                    self._show_frame,
                )
            except Exception as e:
                self.root.after(
                    0, lambda msg=str(e): messagebox.showerror("Camera issue", msg)
                )
            finally:
                self.scanning = False
                self.status("Camera scan stopped.")

        threading.Thread(target=work, daemon=True).start()

    def stop_scan(self):
        self.stop.set()
        self.status("Stopping camera…")

    def autostart(self):
        if (
            MODEL_PATH.exists()
            and LABELS_PATH.exists()
            and not self.scanning
            and not self.job
        ):
            self.show_page("Overview")
            self._start_from("attendance", "Both")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()
