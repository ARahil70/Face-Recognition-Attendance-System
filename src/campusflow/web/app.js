const programmes = {
  Engineering: ["B.Tech", "M.Tech", "Diploma"],
  "Management & Commerce": [
    "BBA",
    "BBA-MBA Integrated",
    "MBA",
    "B.Com",
    "M.Com",
  ],
  "Computer Applications": ["BCA", "BCA-MCA Integrated", "MCA", "PGDCA"],
  "Pharmacy & Health Sciences": [
    "B.Pharm",
    "D.Pharm",
    "B.Pharm (Practice)",
    "M.Pharm",
    "BPT",
    "MPT",
    "B.Sc. Cardiac Care",
    "BMLT",
    "BOT",
    "BRIT",
    "MRIT",
    "M.Sc. MLT",
    "Nursing / Other",
  ],
  "Science & Agriculture": [
    "B.Sc.",
    "M.Sc.",
    "B.Sc. Agriculture",
    "M.Sc. Agriculture",
  ],
  "Education & Psychology": [
    "D.El.Ed.",
    "B.Ed.",
    "M.A. Education",
    "M.A. Psychology",
    "B.P.Ed.",
    "BPES",
    "MPES",
  ],
  Law: ["BA-LLB", "BBA-LLB", "LLB", "LLM"],
  "Humanities & Social Sciences": [
    "BA",
    "MA",
    "BPA",
    "BVA",
    "MPA",
    "MVA",
    "MSW",
  ],
  "Other Faculties": [
    "BA Yoga",
    "MA Yoga",
    "BA Astrology",
    "MA Astrology",
    "Research / Ph.D.",
    "Other / not listed",
  ],
};
const engineering = [
  "Chemical Engineering",
  "Petrochemical Engineering",
  "Civil Engineering",
  "Computer Science & Engineering",
  "Electronics & Communication Engineering",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Mining Engineering",
  "Other / confirm current branch",
];
const branches = {
  "B.Tech": engineering,
  "M.Tech": [
    "Cement & Ceramics",
    "EVS & Engineering",
    "Construction Technology & Management",
    "Environmental Engineering",
    "Structural Engineering",
    "Transportation Engineering",
    "Computer Science & Engineering",
    "Data Science",
    "Digital Communication",
    "VLSI",
    "Other / confirm current branch",
  ],
  Diploma: [
    "Civil Engineering",
    "Computer Science & Engineering",
    "Electrical Engineering",
    "Other / confirm current branch",
  ],
  BBA: [
    "Management",
    "Finance",
    "Marketing",
    "Human Resources",
    "Other / not listed",
  ],
  "BBA-MBA Integrated": [
    "Management",
    "Finance",
    "Marketing",
    "Human Resources",
    "Other / not listed",
  ],
  MBA: [
    "Finance",
    "Marketing",
    "Human Resources",
    "Operations",
    "Other / not listed",
  ],
  "B.Com": ["Commerce"],
  "M.Com": ["Commerce"],
  BCA: ["Computer Applications"],
  "BCA-MCA Integrated": ["Computer Applications"],
  MCA: ["Computer Applications"],
  PGDCA: ["Computer Applications"],
  "B.Pharm": ["Pharmacy"],
  "D.Pharm": ["Pharmacy"],
  "B.Pharm (Practice)": ["Pharmacy Practice"],
  "M.Pharm": ["Pharmaceutics", "Quality Assurance"],
  BPT: ["Physiotherapy"],
  MPT: ["Physiotherapy"],
  "B.Sc. Cardiac Care": ["Cardiac Care"],
  BMLT: ["Medical Laboratory Technology"],
  BOT: ["Occupational Therapy"],
  BRIT: ["Radiology & Imaging Technology"],
  MRIT: ["Radiology & Imaging Technology"],
  "M.Sc. MLT": ["Medical Laboratory Technology"],
  "B.Sc.": [
    "Chemistry",
    "Physics",
    "Mathematics",
    "Biology",
    "Aircraft Maintenance",
    "Other / not listed",
  ],
  "M.Sc.": [
    "Agronomy",
    "Industrial Chemistry",
    "Organic Chemistry",
    "Botany",
    "Environmental Science",
    "Microbiology",
    "Zoology",
    "Mathematics",
    "Physics",
    "Other / not listed",
  ],
  "B.Sc. Agriculture": ["Agriculture"],
  "M.Sc. Agriculture": ["Agronomy"],
  "D.El.Ed.": ["Education"],
  "B.Ed.": ["Education"],
  "M.A. Education": ["Education"],
  "M.A. Psychology": ["Psychology"],
  "B.P.Ed.": ["Physical Education"],
  BPES: ["Physical Education"],
  MPES: ["Physical Education"],
  "BA-LLB": ["Law"],
  "BBA-LLB": ["Law"],
  LLB: ["Law"],
  LLM: ["Law"],
  BA: [
    "Economics",
    "Geography",
    "History",
    "English",
    "Hindi",
    "Political Science",
    "Sociology",
    "Fine Arts",
    "Other / not listed",
  ],
  MA: [
    "Economics",
    "Geography",
    "History",
    "English",
    "Hindi",
    "Political Science",
    "Sociology",
    "Fine Arts",
    "Other / not listed",
  ],
  BPA: ["Performing Arts"],
  BVA: ["Visual Arts"],
  MPA: ["Performing Arts"],
  MVA: ["Visual Arts"],
  MSW: ["Social Work"],
  "BA Yoga": ["Yoga"],
  "MA Yoga": ["Yoga"],
  "BA Astrology": ["Astrology"],
  "MA Astrology": ["Astrology"],
  "Research / Ph.D.": ["Department to confirm"],
  "Other / not listed": ["Specify department / branch"],
};
const facultyBranches = [
  "Chemical Engineering",
  "Civil Engineering",
  "Computer Science & Engineering",
  "Electronics & Communication Engineering",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Mining Engineering",
  "Management",
  "Commerce",
  "Computer Applications",
  "Law",
  "Education",
  "Psychology",
  "Physical Education",
  "Chemistry",
  "Life Science",
  "Mathematics",
  "Physics",
  "Humanities",
  "Economics",
  "Geography",
  "History",
  "Political Science",
  "Sociology",
  "Agriculture",
  "Paramedical",
  "Physiotherapy",
  "Pharmacy",
  "Yoga",
  "Other / not listed",
];
const page = document.querySelector("#page"),
  titles = {
    overview: ["Campus overview", "Your campus attendance at a glance."],
    register: [
      "Register a person",
      "Capture face samples and enter the correct academic details.",
    ],
    attendance: [
      "Attendance entry",
      "Recognize a registered person and record one daily entry.",
    ],
    exit: ["Exit tracking", "Record a person’s departure after attendance."],
    records: [
      "Records & reports",
      "Filter attendance by programme, branch, section and date.",
    ],
    manage: [
      "Manage people",
      "Review active profiles and recover deleted profiles.",
    ],
  };
const IP_CAMERA_URL_KEY = "campusflow.ipWebcamUrl";
const SYSTEM_CAMERA_INDEX_KEY = "campusflow.systemCameraIndex";
const localDate = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
let active = "overview",
  peopleView = "active",
  cached = { people: [], deleted_people: [], records: [], history: [] },
  lastScanError = "",
  lastRegistrationNotice = "",
  reportDate = localDate(),
  reportFilters = { role: "", course: "", branch: "", section: "", search: "" };
const courseChoices = unique([...Object.values(programmes).flat(), "Faculty"]);
const branchChoices = unique([
  ...Object.values(branches).flat(),
  ...facultyBranches,
]);
const sectionChoices = ["A", "B", "C", "D", "Not applicable"];
document.querySelector("#today").textContent = new Date().toLocaleDateString(
  "en-IN",
  { weekday: "short", day: "2-digit", month: "short", year: "numeric" },
);
document
  .querySelectorAll(".nav")
  .forEach((b) => (b.onclick = () => show(b.dataset.page)));
function show(p) {
  active = p;
  document
    .querySelectorAll(".nav")
    .forEach((x) => x.classList.toggle("active", x.dataset.page === p));
  document.querySelector("#crumb").textContent = titles[p][0];
  document.querySelector("#title").textContent = titles[p][0];
  document.querySelector("#subtitle").textContent = titles[p][1];
  render();
}
function toast(t) {
  const x = document.querySelector("#toast");
  x.textContent = t;
  x.classList.add("show");
  setTimeout(() => x.classList.remove("show"), 4500);
}
function updateModelStatus() {
  const chip = document.querySelector("#modelStatus"),
    details = document.querySelector("#modelDetails"),
    retry = document.querySelector("#retryModel");
  if (!chip) return;
  if (cached.training) {
    chip.textContent = "Updating automatically";
    details.textContent =
      "The recognition model is training in the background. Attendance and exit scans will be available when it finishes.";
  } else if (cached.model_ready) {
    chip.textContent = "Up to date";
    details.textContent =
      "The face model updates automatically after a successful new registration.";
  } else if (cached.training_error) {
    chip.textContent = "Update needs attention";
    details.textContent = cached.training_error;
    if (retry) retry.style.display = "inline-block";
  } else if (cached.waiting_for_people) {
    chip.textContent = "Waiting for profiles";
    details.textContent =
      "Register one more person and the model will train automatically.";
  } else {
    chip.textContent = "Preparing automatic update";
    details.textContent =
      "The model trains automatically after a face registration.";
  }
  if (retry && !cached.training_error) retry.style.display = "none";
}
function updateRegistrationStatus() {
  const job = cached.registration;
  if (!job) return;
  const state = document.querySelector("#captureState"),
    bar = document.querySelector("#captureProgressBar"),
    label = document.querySelector("#captureProgressLabel"),
    button = document.querySelector("#registerBtn");
  if (state) state.textContent = job.message;
  if (bar) bar.style.width = `${job.percent || 0}%`;
  if (label)
    label.textContent = `${job.count || 0}/${job.total || 100} clear samples`;
  if (button)
    button.disabled = ["connecting", "capturing", "saving"].includes(
      job.status,
    );
  if (["complete", "error"].includes(job.status)) {
    const noticeKey = `${job.id}:${job.status}`;
    if (lastRegistrationNotice !== noticeKey) {
      lastRegistrationNotice = noticeKey;
      toast(
        job.status === "complete"
          ? job.message
          : `Registration failed: ${job.message}`,
      );
    }
  }
}
async function api(data) {
  const r = await fetch("/api/action", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const j = await r.json();
  if (!r.ok) throw Error(j.error || "Request failed");
  return j;
}
async function refresh(force = false) {
  try {
    const day =
      document.querySelector("#dateFilter")?.value ||
      (active === "records" ? reportDate : localDate());
    const r = await fetch("/api/data?date=" + encodeURIComponent(day));
    cached = await r.json();
    document.querySelector("#status").textContent = cached.scanning
      ? "Camera scan active"
      : cached.registration &&
          ["connecting", "capturing", "saving"].includes(
            cached.registration.status,
          )
        ? `Face capture: ${cached.registration.count}/${cached.registration.total}`
        : "System ready";
    const chip = document.querySelector("#scanChip");
    if (chip)
      chip.textContent = cached.scanning ? "● Camera active" : "● Ready";
    const scanStatus = document.querySelector("#scanStatus");
    if (scanStatus && cached.scanning && cached.scan_status)
      scanStatus.textContent = cached.scan_status;
    else if (scanStatus && !cached.scanning)
      scanStatus.textContent =
        "Press Q or Esc in the camera window, or use Stop scan here.";
    updateModelStatus();
    updateRegistrationStatus();
    if (cached.scan_error && cached.scan_error !== lastScanError) {
      lastScanError = cached.scan_error;
      toast("Camera scan stopped: " + lastScanError);
    }
    if (force || active === "overview") render();
  } catch (e) {
    document.querySelector("#status").textContent = "Backend disconnected";
  }
}
function esc(s) {
  return String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
}
function initials(n) {
  return String(n || "?")
    .split(/\s+/)
    .slice(0, 2)
    .map((x) => x[0])
    .join("")
    .toUpperCase();
}
function filterPeople(people, opts = {}) {
  const role = opts.role || "",
    course = opts.course || "",
    branch = opts.branch || "",
    section = opts.section || "",
    q = (opts.search || "").toLowerCase();
  return people.filter(
    (p) =>
      (!role || p[2] === role) &&
      (!course || (course === "__legacy__" ? !p[4] : p[4] === course)) &&
      (!branch || (branch === "__legacy__" ? !p[5] : p[5] === branch)) &&
      (!section || (section === "__legacy__" ? !p[6] : p[6] === section)) &&
      (!q || [p[0], ...p.slice(1)].join(" ").toLowerCase().includes(q)),
  );
}
function tableRows(records) {
  return (
    records
      .map(
        (r) =>
          `<tr><td><b>${esc(r[1])}</b></td><td>${esc(r[2])}</td><td>${esc([r[6], r[7], r[8]].filter(Boolean).join(" · ") || "—")}</td><td>${r[3] === "P" ? '<span class="badge">Present</span>' : '<span class="badge" style="background:#fff1ef;color:#d45d54">Absent</span>'}</td><td>${esc(r[4] || "—")}</td><td>${esc(r[5] || "—")}</td></tr>`,
      )
      .join("") ||
    '<tr><td colspan="6" class="empty">No attendance records match these filters.</td></tr>'
  );
}
function courseOptions(role = "Student", selected = "") {
  if (role === "Faculty")
    return '<option value="Faculty" selected>Faculty</option>';
  return Object.entries(programmes)
    .map(
      ([group, list]) =>
        `<optgroup label="${esc(group)}">${list.map((c) => `<option ${c === selected ? "selected" : ""}>${esc(c)}</option>`).join("")}</optgroup>`,
    )
    .join("");
}
function branchOptions(course, role = "Student", selected = "") {
  const list =
    role === "Faculty"
      ? facultyBranches
      : branches[course] || ["Other / not listed"];
  return list
    .map(
      (b) => `<option ${b === selected ? "selected" : ""}>${esc(b)}</option>`,
    )
    .join("");
}
function selectFilter(id, label, values, legacy = false) {
  return `<select id="${id}"><option value="">All ${label}</option>${values.map((v) => `<option>${esc(v)}</option>`).join("")}${legacy ? '<option value="__legacy__">Legacy / not entered</option>' : ""}</select>`;
}
function unique(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) =>
    a.localeCompare(b),
  );
}
function filterTableByHierarchy(id, filters, baseRows) {
  const filtered = baseRows.filter(
    (r) =>
      (!filters.role || r[2] === filters.role) &&
      (!filters.course ||
        (filters.course === "__legacy__" ? !r[6] : r[6] === filters.course)) &&
      (!filters.branch ||
        (filters.branch === "__legacy__" ? !r[7] : r[7] === filters.branch)) &&
      (!filters.section ||
        (filters.section === "__legacy__"
          ? !r[8]
          : r[8] === filters.section)) &&
      (!filters.search ||
        r[1].toLowerCase().includes(filters.search.toLowerCase())),
  );
  document.querySelector("#" + id).innerHTML = tableRows(filtered);
  return filtered;
}
function render() {
  page.className = "";
  const people = cached.people || [],
    rs = cached.records || [],
    history = cached.history || [],
    present = rs.filter((r) => r[3] === "P"),
    absent = rs.filter((r) => r[3] === "A");
  if (active === "overview") {
    page.innerHTML = `<div class="grid stats"><div class="card metric" style="--tint:#eaf0ff;--accent:#4778f5"><div class="icon">♙</div><label>Registered people</label><strong>${people.length}</strong><span class="hint">Students & faculty</span></div><div class="card metric" style="--tint:#e5f8f2;--accent:#16a587"><div class="icon">✓</div><label>Present today</label><strong>${present.length}</strong><span class="hint">${rs.length ? Math.round((present.length * 100) / rs.length) : 0}% attendance</span></div><div class="card metric" style="--tint:#fff3e6;--accent:#e69a35"><div class="icon">◷</div><label>Absent today</label><strong>${absent.length}</strong><span class="hint">Across campus</span></div><div class="card metric" style="--tint:#f1ebff;--accent:#8c62dd"><div class="icon">↗</div><label>Exited today</label><strong>${rs.filter((r) => r[5]).length}</strong><span class="hint">Exit recorded</span></div></div><div class="grid columns"><div class="card"><div class="card-head"><div><h2>Today’s attendance</h2><p>Live daily status by person</p></div><span class="chip">${new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "short" })}</span></div><div class="toolbar"><select id="roleFilter"><option value="">All people</option><option>Student</option><option>Faculty</option></select><input id="search" placeholder="Search name, course, branch…"></div><div class="table-wrap"><table><thead><tr><th>Name</th><th>Role</th><th>Course · branch · section</th><th>Status</th><th>Entry</th><th>Exit</th></tr></thead><tbody id="todayRows">${tableRows(rs)}</tbody></table></div></div><div class="card"><div class="card-head"><div><h2>Quick actions</h2><p>Common campus tasks</p></div></div><div class="quick"><button onclick="show('register')">＋ &nbsp; Register person</button><button onclick="show('attendance')">◎ &nbsp; Mark attendance</button><button onclick="show('exit')">↗ &nbsp; Record exit</button><button onclick="show('records')">▤ &nbsp; View records</button></div><h3 class="section-title">Recently registered</h3>${
      people
        .slice(-5)
        .reverse()
        .map(
          (p) =>
            `<div class="row"><div class="person-avatar">${initials(p[1])}</div><div class="row-main"><b>${esc(p[1])}</b><small>${esc([p[2], p[4], p[5], p[6]].filter(Boolean).join(" · "))} · Added ${String(p[3]).slice(0, 10)}</small></div></div>`,
        )
        .join("") || '<p class="muted">Register your first person to begin.</p>'
    }</div></div>`;
    const apply = () => {
      const q = document.querySelector("#search").value.toLowerCase(),
        role = document.querySelector("#roleFilter").value;
      document.querySelector("#todayRows").innerHTML = tableRows(
        rs.filter(
          (r) =>
            (!role || r[2] === role) &&
            JSON.stringify(r).toLowerCase().includes(q),
        ),
      );
    };
    document.querySelector("#search").oninput = apply;
    document.querySelector("#roleFilter").onchange = apply;
  } else if (active === "register") {
    page.innerHTML = `<div class="card"><h2 class="panel-title">New campus profile</h2><p class="panel-note">Select the course name first, then choose its branch, section and camera source.</p><div class="form-grid"><div class="field"><label>Full name *</label><input id="name" placeholder="Enter name as on university ID"></div><div class="field"><label>Person type *</label><select id="role"><option>Student</option><option>Faculty</option></select></div><div class="field"><label>Course *</label><select id="course"><option value="">Choose course</option>${courseOptions()}</select></div><div class="field"><label>Branch / department *</label><select id="branch"><option>Choose course first</option></select></div><div class="field"><label>Section *</label><select id="section"><option>A</option><option>B</option><option>C</option><option>D</option><option>Not applicable</option></select></div><div class="field"><label>Camera source</label><select id="camera"><option>System camera</option><option>IP Webcam</option></select></div><div class="field full" id="sourceWrap" style="display:none"><label>IP Webcam URL (base, /shot.jpg or /video)</label><input id="source" placeholder="http://phone-ip:8080"></div><div class="full callout">Keep the phone and computer on the same Wi-Fi and leave the IP Webcam server running. The last phone address is remembered across registration, attendance and exit; update it if the phone IP changes. The app accepts the base URL, /shot.jpg snapshot URL, or /video stream URL. Camera connection and sample progress appear in the camera window. Keep one face in frame; blurry or unclear samples are rejected.</div><div class="full capture-progress"><div class="capture-progress-head"><span id="captureState" role="status">100 clear samples are collected at a measured pace.</span><b id="captureProgressLabel">0/100 clear samples</b></div><div class="capture-progress-track"><span id="captureProgressBar"></span></div></div><div class="full split"><button class="action" id="registerBtn">Capture face & register</button><span class="muted">Keep this page open while capture is running.</span></div></div></div><div class="card" style="margin-top:18px"><div class="card-head"><div><h2>Recognition model</h2><p>Face model updates automatically after a successful new registration.</p></div><span class="chip" id="modelStatus">Checking status…</span></div><p class="panel-note" id="modelDetails">Waiting for model status…</p><button class="action gray" id="retryModel" style="display:none">Retry model update</button></div>`;
    const role = document.querySelector("#role"),
      course = document.querySelector("#course"),
      branch = document.querySelector("#branch"),
      section = document.querySelector("#section");
    function updateRole() {
      const faculty = role.value === "Faculty";
      course.innerHTML = faculty
        ? '<option value="Faculty">Faculty</option>'
        : '<option value="">Choose course</option>' + courseOptions();
      if (faculty) {
        course.value = "Faculty";
        section.value = "Not applicable";
      }
      updateBranch();
    }
    function updateBranch() {
      branch.innerHTML = course.value
        ? branchOptions(course.value, role.value)
        : "<option>Choose course first</option>";
    }
    role.onchange = updateRole;
    course.onchange = updateBranch;
    updateRole();
    const registerCamera = document.querySelector("#camera"),
      registerSource = document.querySelector("#source"),
      sourceWrap = document.querySelector("#sourceWrap");
    registerSource.value = localStorage.getItem(IP_CAMERA_URL_KEY) || "";
    registerSource.oninput = () => {
      const value = registerSource.value.trim();
      if (value) localStorage.setItem(IP_CAMERA_URL_KEY, value);
      else localStorage.removeItem(IP_CAMERA_URL_KEY);
    };
    registerCamera.onchange = () => {
      sourceWrap.style.display =
        registerCamera.value === "IP Webcam" ? "flex" : "none";
    };
    document.querySelector("#registerBtn").onclick = async () => {
      const name = document.querySelector("#name").value.trim(),
        who = role.value,
        courseValue = course.value,
        branchValue = branch.value,
        sectionValue = section.value,
        camera = document.querySelector("#camera").value,
        source =
          camera === "IP Webcam" ? registerSource.value.trim() : "0";
      if (!name || !courseValue || !branchValue)
        return toast("Enter the name and select course and branch first.");
      if (camera === "IP Webcam" && !source)
        return toast("Enter the current IP Webcam address shown on your phone.");
      if (camera === "IP Webcam")
        localStorage.setItem(IP_CAMERA_URL_KEY, source);
      const btn = document.querySelector("#registerBtn"),
        state = document.querySelector("#captureState");
      btn.disabled = true;
      state.textContent = "Starting the camera and checking its connection…";
      try {
        const x = await api({
          action: "register",
          name,
          role: who,
          course: courseValue,
          branch: branchValue,
          section: sectionValue,
          camera,
          source,
        });
        state.textContent = x.message;
        let job = null;
        while (!job || !["complete", "error"].includes(job.status)) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          const day = document.querySelector("#dateFilter")?.value || localDate();
          const result = await fetch(
            "/api/data?date=" + encodeURIComponent(day),
          );
          cached = await result.json();
          updateModelStatus();
          updateRegistrationStatus();
          job = cached.registration;
          if (!job || job.id !== x.registration_id) break;
        }
        await refresh();
      } catch (e) {
        state.textContent = `Could not start capture: ${e.message}`;
        toast(e.message);
      } finally {
        if (document.querySelector("#registerBtn"))
          document.querySelector("#registerBtn").disabled = false;
      }
    };
    document.querySelector("#retryModel").onclick = async () => {
      const b = document.querySelector("#retryModel");
      b.disabled = true;
      try {
        toast((await api({ action: "train" })).message);
        await refresh();
      } catch (e) {
        toast(e.message);
      } finally {
        b.disabled = false;
      }
    };
  } else if (active === "attendance" || active === "exit") {
    const isExit = active === "exit";
    const exited = rs.filter((r) => r[5]),
      onCampus = present.filter((r) => !r[5]);
    page.className = isExit
      ? "scan-screen exit-screen"
      : "scan-screen attendance-screen";

    if (isExit) {
      const recentDepartures = exited
        .slice()
        .sort((a, b) => String(b[5]).localeCompare(String(a[5])))
        .slice(0, 6);
      const departureRows =
        recentDepartures
          .map(
            (r) =>
              '<div class="departure-row"><span class="departure-avatar">' +
              esc(initials(r[1])) +
              '</span><div class="departure-person"><b>' +
              esc(r[1]) +
              '</b><small>' +
              esc(r[2]) +
              ' · ' +
              esc(r[6] || r[7] || "Campus") +
              '</small></div><time>' +
              esc(r[5]) +
              "</time></div>",
          )
          .join("") ||
        '<div class="departure-empty"><span>↗</span><b>No departures recorded yet</b><small>Exit scans will appear here as people leave.</small></div>';

      page.innerHTML = `
        <div class="exit-heading">
          <div><span class="scan-eyebrow exit-eyebrow">DEPARTURE DESK · TODAY</span><h2>Campus exit scan</h2><p>Record each person’s departure and keep today’s exit log up to date.</p></div>
          <div class="exit-heading-mark"><span>↗</span><small>CHECK OUT</small></div>
        </div>
        <div class="exit-stats">
          <div class="exit-stat"><span>⌂</span><div><small>ON CAMPUS</small><b>${onCampus.length}</b></div></div>
          <div class="exit-stat"><span>↗</span><div><small>EXITED TODAY</small><b>${exited.length}</b></div></div>
          <div class="exit-stat"><span>◷</span><div><small>NO ENTRY TODAY</small><b>${absent.length}</b></div></div>
        </div>
        <div class="exit-layout">
          <section class="exit-camera-panel">
            <div class="exit-camera-title"><div class="exit-camera-icon">↗</div><div><span class="scan-eyebrow">EXIT RECORDING</span><h3>Record a departure</h3><p>Only a registered person with today’s attendance can be checked out.</p></div><span class="chip exit-chip" id="scanChip">● Ready</span></div>
            <div class="exit-steps"><div><i>01</i><span>Face in frame</span></div><div><i>02</i><span>Identity matched</span></div><div><i>03</i><span>Exit time saved</span></div></div>
            <div class="scan-source-grid"><div class="field"><label>Camera source</label><select id="scanCamera"><option>System camera</option><option>IP Webcam</option></select></div><div class="field"><label id="cameraSourceLabel">System camera index</label><input id="cameraSource" value="0" placeholder="0"><small class="muted camera-source-hint" id="cameraSourceHint">Use 0 for the default camera.</small></div></div>
            <div class="exit-camera-note">Keep one person in front of the camera. The exit time is stored separately.</div>
            <div class="scan-action-row"><button class="action orange" id="startScan">Start exit scan</button><button class="action gray" id="stopScan">Stop scan</button></div>
            <p class="scan-help" id="scanStatus">Connecting to camera…</p>
          </section>
          <aside class="card departures-card">
            <div class="departure-card-head"><div><span class="scan-eyebrow exit-text-eyebrow">LIVE EXIT LOG</span><h3>Today’s departures</h3></div><span class="departure-count">${exited.length}</span></div>
            <div class="departure-list">${departureRows}</div>
            <button class="action gray departure-records" onclick="show('records')">View full daily report <span>→</span></button>
          </aside>
        </div>`;
    } else {
      page.innerHTML = `
        <div class="attendance-hero">
          <div><span class="scan-eyebrow attendance-eyebrow">DAILY CHECK-IN · STUDENTS & FACULTY</span><h2>Attendance station</h2><p>Recognize registered people and record today’s attendance once per person.</p>
            <div class="attendance-hero-stats"><div><b>${rs.length}</b><span>Expected</span></div><div><b>${present.length}</b><span>Present</span></div><div><b>${absent.length}</b><span>Not checked in</span></div></div>
          </div>
          <div class="attendance-hero-mark"><span>◎</span><small>CHECK IN</small></div>
        </div>
        <div class="attendance-layout">
          <section class="card checkin-panel">
            <div class="checkin-title"><div class="checkin-step">01</div><div class="checkin-heading"><span class="scan-eyebrow attendance-text-eyebrow">ATTENDANCE SCAN</span><h3>Start today’s check-in</h3><p>Choose the camera and let the system recognize each person.</p></div><span class="chip" id="scanChip">● Ready</span></div>
            <div class="scan-source-grid"><div class="field"><label>Camera source</label><select id="scanCamera"><option>System camera</option><option>IP Webcam</option></select></div><div class="field"><label id="cameraSourceLabel">System camera index</label><input id="cameraSource" value="0" placeholder="0"><small class="muted camera-source-hint" id="cameraSourceHint">Use 0 for the default camera.</small></div></div>
            <div class="checkin-camera-note"><span>⌖</span><div><b>Camera ready when you are</b><small>A separate live camera window opens when the scan starts. Keep one person in frame for a clear match.</small></div></div>
            <div class="scan-action-row"><button class="action teal" id="startScan">Start attendance scan</button><button class="action gray" id="stopScan">Stop scan</button></div>
            <p class="scan-help" id="scanStatus">Connecting to camera…</p>
          </section>
          <aside class="attendance-side">
            <div class="card attendance-live-card"><div class="attendance-side-head"><span class="attendance-side-icon">✓</span><div><span class="scan-eyebrow attendance-text-eyebrow">TODAY’S LIVE TALLY</span><h3>Campus check-in</h3></div></div>
              <div class="live-tally"><div><b>${present.length}</b><span>Marked present</span></div><div><b>${absent.length}</b><span>Still absent</span></div></div>
              <div class="tally-progress"><span style="width:${rs.length ? Math.round((present.length * 100) / rs.length) : 0}%"></span></div><small class="tally-caption">${rs.length ? Math.round((present.length * 100) / rs.length) : 0}% of today’s registered people checked in</small>
            </div>
            <div class="attendance-rule-card"><span>i</span><div><b>One check-in per day</b><p>Repeated scans won’t create a second attendance entry for the same person today.</p><button onclick="show('records')">Open attendance records →</button></div></div>
          </aside>
        </div>`;
    }

    const scanCamera = document.querySelector("#scanCamera"),
      scanSource = document.querySelector("#cameraSource"),
      scanSourceLabel = document.querySelector("#cameraSourceLabel"),
      scanSourceHint = document.querySelector("#cameraSourceHint");
    function updateScanSourceField() {
      if (scanCamera.value === "IP Webcam") {
        scanSource.value = localStorage.getItem(IP_CAMERA_URL_KEY) || "";
        scanSource.placeholder = "http://phone-ip:8080";
        scanSourceLabel.textContent = "IP Webcam URL";
        scanSourceHint.textContent =
          "Use the phone's current address. A base URL or /shot.jpg works.";
      } else {
        scanSource.value =
          localStorage.getItem(SYSTEM_CAMERA_INDEX_KEY) || "0";
        scanSource.placeholder = "0";
        scanSourceLabel.textContent = "System camera index";
        scanSourceHint.textContent = "Use 0 for the default camera.";
      }
    }
    scanCamera.onchange = updateScanSourceField;
    scanSource.oninput = () => {
      const value = scanSource.value.trim();
      if (scanCamera.value === "IP Webcam") {
        if (value) localStorage.setItem(IP_CAMERA_URL_KEY, value);
        else localStorage.removeItem(IP_CAMERA_URL_KEY);
      } else {
        localStorage.setItem(SYSTEM_CAMERA_INDEX_KEY, value || "0");
      }
    };
    updateScanSourceField();

    document.querySelector("#startScan").onclick = async () => {
      const camera = scanCamera.value,
        source = scanSource.value.trim();
      if (camera === "IP Webcam" && !source)
        return toast("Enter the current IP Webcam address shown on your phone.");
      if (camera === "IP Webcam")
        localStorage.setItem(IP_CAMERA_URL_KEY, source);
      else localStorage.setItem(SYSTEM_CAMERA_INDEX_KEY, source || "0");
      try {
        const a = await api({
          action: isExit ? "exit" : "attendance",
          camera,
          source: source || "0",
        });
        toast(a.message);
        refresh();
      } catch (e) {
        toast(e.message);
      }
    };
    document.querySelector("#stopScan").onclick = async () => {
      try {
        toast((await api({ action: "stop" })).message);
        refresh();
      } catch (e) {
        toast(e.message);
      }
    };
  } else if (active === "records") {
    const courses = courseChoices,
      allBranches = branchChoices,
      sections = sectionChoices;
    page.innerHTML = `<div class="card"><div class="card-head"><div><h2>Department attendance report</h2><p>Filter by course, branch and section to see exactly that student group.</p></div><button class="action gray" id="exportBtn">↓ Export filtered CSV</button></div><div class="toolbar" style="flex-wrap:wrap"><input type="date" id="dateFilter" value="${reportDate}"><select id="recordRole"><option value="">Students + faculty</option><option>Student</option><option>Faculty</option></select>${selectFilter("recordCourse", "courses", courses, true)}${selectFilter("recordBranch", "branches", allBranches, true)}${selectFilter("recordSection", "sections", sections, true)}<input id="recordSearch" placeholder="Search person name"></div><div class="split"><span class="chip" id="presentCount">Present ${present.length}</span><span class="chip" style="background:#fff1ef;color:#d45d54" id="absentCount">Absent ${absent.length}</span><span class="chip" style="background:#f2edff;color:#8155d7" id="exitCount">Exited ${rs.filter((r) => r[5]).length}</span></div><h3 class="section-title">Selected date — <span id="filteredGroup">All campus</span></h3><div class="table-wrap"><table><thead><tr><th>Name</th><th>Role</th><th>Course · branch · section</th><th>Status</th><th>Entry time</th><th>Exit time</th></tr></thead><tbody id="recordRows">${tableRows(rs)}</tbody></table></div><h3 class="section-title">Individual attendance history</h3><p class="panel-note">Choose a student to see each recorded attendance date and the total number of days present.</p><div class="form-grid"><div class="field"><label>Student in selected department/group</label><select id="studentHistory"><option value="">Choose a person</option></select></div><div class="card" style="box-shadow:none;background:#f6f8fc"><span class="muted">Recorded attendance days</span><h2 id="daysCount" style="margin:8px 0 0">—</h2></div></div><div class="table-wrap" style="margin-top:14px"><table><thead><tr><th>Date</th><th>Name</th><th>Role</th><th>Status</th><th>Entry</th><th>Exit</th></tr></thead><tbody id="personHistoryRows"><tr><td colspan="6" class="empty">Select a student to see their history.</td></tr></tbody></table></div></div>`;
    const ids = [
      "recordRole",
      "recordCourse",
      "recordBranch",
      "recordSection",
      "recordSearch",
    ];
    document.querySelector("#recordRole").value = reportFilters.role;
    document.querySelector("#recordCourse").value = reportFilters.course;
    document.querySelector("#recordBranch").value = reportFilters.branch;
    document.querySelector("#recordSection").value = reportFilters.section;
    document.querySelector("#recordSearch").value = reportFilters.search;
    const getFilters = () => ({
      role: document.querySelector("#recordRole").value,
      course: document.querySelector("#recordCourse").value,
      branch: document.querySelector("#recordBranch").value,
      section: document.querySelector("#recordSection").value,
      search: document.querySelector("#recordSearch").value,
    });
    function applyFilters() {
      const f = getFilters();
      reportFilters = f;
      const visible = filterTableByHierarchy("recordRows", f, rs),
        attended = visible.filter((r) => r[3] === "P").length,
        missed = visible.filter((r) => r[3] === "A").length;
      document.querySelector("#presentCount").textContent =
        "Present " + attended;
      document.querySelector("#absentCount").textContent = "Absent " + missed;
      document.querySelector("#exitCount").textContent =
        "Exited " + visible.filter((r) => r[5]).length;
      document.querySelector("#filteredGroup").textContent =
        [f.course, f.branch, f.section].filter(Boolean).join(" / ") ||
        "All campus";
      const roster = filterPeople(people, f).filter(
        (p) => !f.role || p[2] === f.role,
      );
      const dropdown = document.querySelector("#studentHistory"),
        prev = dropdown.value;
      dropdown.innerHTML =
        '<option value="">Choose a person</option>' +
        roster
          .map(
            (p) =>
              `<option value="${p[0]}">${esc(p[1])} · ${esc([p[2], p[4], p[5], p[6]].filter(Boolean).join(" / "))}</option>`,
          )
          .join("");
      if (roster.some((p) => p[0] === prev)) dropdown.value = prev;
      showPersonHistory(dropdown.value);
    }
    function showPersonHistory(pid) {
      const tbody = document.querySelector("#personHistoryRows");
      if (!pid) {
        document.querySelector("#daysCount").textContent = "—";
        tbody.innerHTML =
          '<tr><td colspan="6" class="empty">Select a student to see their history.</td></tr>';
        return;
      }
      const own = history.filter((h) => h[1] === pid),
        days = own.filter((h) => h[4] === "P");
      document.querySelector("#daysCount").textContent = days.length + " days";
      tbody.innerHTML =
        own
          .map(
            (h) =>
              `<tr><td>${esc(h[0])}</td><td><b>${esc(h[2])}</b></td><td>${esc(h[3])}</td><td>${h[4] === "P" ? '<span class="badge">Present</span>' : '<span class="badge" style="background:#fff1ef;color:#d45d54">Absent</span>'}</td><td>${esc(h[5] || "—")}</td><td>${esc(h[6] || "—")}</td></tr>`,
          )
          .join("") ||
        '<tr><td colspan="6" class="empty">No daily records yet.</td></tr>';
    }
    ids.forEach(
      (id) =>
        (document.querySelector("#" + id).oninput = () => {
          applyFilters();
        }),
    );
    document.querySelector("#dateFilter").onchange = () => {
      reportDate = document.querySelector("#dateFilter").value;
      refresh(true);
    };
    document.querySelector("#studentHistory").onchange = (e) =>
      showPersonHistory(e.target.value);
    document.querySelector("#exportBtn").onclick = () =>
      exportFiltered(rs, getFilters());
    applyFilters();
  } else if (active === "manage") {
    renderManage(people);
  }
}

function renderManage(people) {
  const deleted = cached.deleted_people || [],
    courses = courseChoices,
    branchesList = branchChoices,
    sections = sectionChoices;
  page.innerHTML = `<div class="card"><div class="card-head"><div><h2>People directory</h2><p>Manage registered profiles and recover accidentally removed people.</p></div><span class="chip">${people.length} active</span></div><div class="split" style="margin-bottom:16px;flex-wrap:wrap"><button class="action ${peopleView === "active" ? "" : "gray"}" id="activePeopleTab">Active profiles · ${people.length}</button><button class="action ${peopleView === "trash" ? "orange" : "gray"}" id="recycleBinTab">Recycle Bin · ${deleted.length}</button></div>${peopleView === "active" ? `<div class="toolbar" style="flex-wrap:wrap"><select id="manageRole"><option value="">All roles</option><option>Student</option><option>Faculty</option></select>${selectFilter("manageCourse", "courses", courses, true)}${selectFilter("manageBranch", "departments / branches", branchesList, true)}${selectFilter("manageSection", "sections", sections, true)}<input id="manageSearch" placeholder="Search name or ID"></div><div class="table-wrap"><table><thead><tr><th>Name</th><th>Role</th><th>Course</th><th>Branch / department</th><th>Section</th><th>Registered</th><th>Action</th></tr></thead><tbody id="peopleRows"></tbody></table></div><div class="callout" style="margin-top:16px">Moving a profile to the Recycle Bin stops recognition but preserves its face samples and attendance history. Restore it any time from the Recycle Bin.</div>` : `<div class="callout" style="margin-bottom:16px">Deleted profiles are kept here with their face samples and attendance history. Restore brings the person back into recognition. Permanently delete erases that profile and its history from this app.</div><div class="toolbar"><input id="deletedSearch" placeholder="Search deleted name or ID"><span class="muted">${deleted.length} saved profile${deleted.length === 1 ? "" : "s"}</span></div><div class="table-wrap"><table><thead><tr><th>Name</th><th>Role</th><th>Course</th><th>Branch / department</th><th>Section</th><th>Deleted</th><th>Action</th></tr></thead><tbody id="deletedRows"></tbody></table></div>`}</div><dialog id="profileEditor" class="profile-dialog"><div class="card"><h2>Edit academic details</h2><p class="panel-note">This updates the person’s course grouping; it does not change their face samples.</p><div class="form-grid"><div class="field"><label>Course</label><select id="editCourse"></select></div><div class="field"><label>Branch / department</label><select id="editBranch"></select></div><div class="field"><label>Section</label><select id="editSection"><option>A</option><option>B</option><option>C</option><option>D</option><option>Not applicable</option></select></div></div><div class="split" style="margin-top:18px"><button class="action" id="saveProfile">Save details</button><button class="action gray" id="cancelProfile">Cancel</button></div></div></dialog>`;
  document.querySelector("#activePeopleTab").onclick = () => {
    peopleView = "active";
    renderManage(people);
  };
  document.querySelector("#recycleBinTab").onclick = () => {
    peopleView = "trash";
    renderManage(people);
  };
  function applyPeople() {
    const f = {
        role: document.querySelector("#manageRole").value,
        course: document.querySelector("#manageCourse").value,
        branch: document.querySelector("#manageBranch").value,
        section: document.querySelector("#manageSection").value,
        search: document.querySelector("#manageSearch").value,
      },
      filtered = filterPeople(people, f);
    document.querySelector("#peopleRows").innerHTML =
      filtered
        .map(
          (p) =>
            `<tr><td><b>${esc(p[1])}</b></td><td>${esc(p[2])}</td><td>${esc(p[4] || "—")}</td><td>${esc(p[5] || "—")}</td><td>${esc(p[6] || "—")}</td><td>${esc(String(p[3]).slice(0, 10))}</td><td><div class="split"><button class="action gray edit-person" data-id="${esc(p[0])}" style="padding:7px 11px">Edit details</button><button class="action orange delete-person" data-id="${esc(p[0])}" data-name="${esc(p[1])}" style="padding:7px 11px">Move to Recycle Bin</button></div></td></tr>`,
        )
        .join("") ||
      '<tr><td colspan="7" class="empty">No registered people match these filters.</td></tr>';
    document
      .querySelectorAll(".edit-person")
      .forEach(
        (b) =>
          (b.onclick = () =>
            openProfileEditor(people.find((p) => p[0] === b.dataset.id))),
      );
    document.querySelectorAll(".delete-person").forEach(
      (b) =>
        (b.onclick = async () => {
          const name = b.dataset.name;
          if (
            !confirm(
              `Move ${name} to the Recycle Bin? Their face samples and attendance history will be kept, and they can be restored later.`,
            )
          )
            return;
          try {
            const result = await api({
              action: "delete_person",
              person_id: b.dataset.id,
            });
            peopleView = "trash";
            toast(result.message);
            await refresh(true);
          } catch (e) {
            toast(e.message);
          }
        }),
    );
  }
  function applyDeleted() {
    const q = document.querySelector("#deletedSearch").value.toLowerCase(),
      filtered = deleted.filter(
        (p) => !q || p.slice(0, 8).join(" ").toLowerCase().includes(q),
      );
    document.querySelector("#deletedRows").innerHTML =
      filtered
        .map(
          (p) =>
            `<tr><td><b>${esc(p[1])}</b></td><td>${esc(p[2])}</td><td>${esc(p[5] || "—")}</td><td>${esc(p[6] || "—")}</td><td>${esc(p[7] || "—")}</td><td>${esc(
              String(p[4] || "")
                .replace("T", " ")
                .slice(0, 16),
            )}</td><td><div class="split"><button class="action teal restore-person" data-id="${esc(p[0])}" data-name="${esc(p[1])}" style="padding:7px 11px">Restore</button><button class="action orange purge-person" data-id="${esc(p[0])}" data-name="${esc(p[1])}" style="padding:7px 11px">Permanently delete</button></div></td></tr>`,
        )
        .join("") ||
      '<tr><td colspan="7" class="empty">Recycle Bin is empty.</td></tr>';
    document.querySelectorAll(".restore-person").forEach(
      (b) =>
        (b.onclick = async () => {
          try {
            const result = await api({
              action: "restore_person",
              person_id: b.dataset.id,
            });
            peopleView = "active";
            toast(result.message);
            await refresh(true);
          } catch (e) {
            toast(e.message);
          }
        }),
    );
    document.querySelectorAll(".purge-person").forEach(
      (b) =>
        (b.onclick = async () => {
          if (
            !confirm(
              `Permanently delete ${b.dataset.name}? This cannot be undone and erases their face samples and attendance/exit history.`,
            )
          )
            return;
          try {
            toast(
              (
                await api({
                  action: "permanently_delete_person",
                  person_id: b.dataset.id,
                })
              ).message,
            );
            await refresh(true);
          } catch (e) {
            toast(e.message);
          }
        }),
    );
  }
  function openProfileEditor(person) {
    const dlg = document.querySelector("#profileEditor"),
      c = document.querySelector("#editCourse"),
      b = document.querySelector("#editBranch"),
      sec = document.querySelector("#editSection");
    c.innerHTML =
      person[2] === "Faculty"
        ? '<option value="Faculty">Faculty</option>'
        : '<option value="">Choose course</option>' + courseOptions();
    c.value = person[2] === "Faculty" ? "Faculty" : person[4];
    b.innerHTML =
      '<option value="">Choose department / branch</option>' +
      branchOptions(c.value, person[2]);
    b.value = person[5] || "";
    sec.value = person[6] || "Not applicable";
    c.onchange = () => {
      b.innerHTML =
        '<option value="">Choose department / branch</option>' +
        branchOptions(c.value, person[2]);
    };
    document.querySelector("#cancelProfile").onclick = () => dlg.close();
    document.querySelector("#saveProfile").onclick = async () => {
      if (!c.value || !b.value)
        return toast("Select course and branch/department first.");
      try {
        toast(
          (
            await api({
              action: "update_profile",
              person_id: person[0],
              course: c.value,
              branch: b.value,
              section: sec.value,
            })
          ).message,
        );
        dlg.close();
        await refresh(true);
        show("manage");
      } catch (e) {
        toast(e.message);
      }
    };
    dlg.showModal();
  }
  if (peopleView === "active") {
    [
      "manageRole",
      "manageCourse",
      "manageBranch",
      "manageSection",
      "manageSearch",
    ].forEach((id) => {
      const el = document.querySelector("#" + id);
      el.oninput = applyPeople;
      el.onchange = applyPeople;
    });
    applyPeople();
  } else {
    document.querySelector("#deletedSearch").oninput = applyDeleted;
    applyDeleted();
  }
}

function exportFiltered(records, filters) {
  const selected = records.filter(
    (r) =>
      (!filters.role || r[2] === filters.role) &&
      (!filters.course ||
        (filters.course === "__legacy__" ? !r[6] : r[6] === filters.course)) &&
      (!filters.branch ||
        (filters.branch === "__legacy__" ? !r[7] : r[7] === filters.branch)) &&
      (!filters.section ||
        (filters.section === "__legacy__"
          ? !r[8]
          : r[8] === filters.section)) &&
      (!filters.search ||
        r[1].toLowerCase().includes(filters.search.toLowerCase())),
  );
  const rows = [
      [
        "Date",
        "Name",
        "Role",
        "Course",
        "Branch",
        "Section",
        "Status",
        "Entry",
        "Exit",
      ],
      ...selected.map((r) => [
        r[0],
        r[1],
        r[2],
        r[6],
        r[7],
        r[8],
        r[3],
        r[4],
        r[5],
      ]),
    ],
    csv = rows
      .map((r) =>
        r
          .map((x) => '"' + String(x ?? "").replaceAll('"', '""') + '"')
          .join(","),
      )
      .join("\r\n"),
    a = document.createElement("a");
  a.href = URL.createObjectURL(
    new Blob(["\ufeff" + csv], { type: "text/csv" }),
  );
  a.download =
    "mewar-attendance-" +
    (document.querySelector("#dateFilter")?.value || localDate()) +
    ".csv";
  a.click();
  URL.revokeObjectURL(a.href);
}
if (location.protocol === "file:") {
  page.innerHTML =
    '<div class="card" style="max-width:760px;margin:70px auto;padding:36px"><div class="logo" style="color:white">C</div><h2 style="margin-top:20px">Start CampusFlow to load live records</h2><p class="sub">This HTML preview cannot connect to your attendance database or camera. Run the desktop launcher from the project folder, then use the local dashboard link below.</p><div class="callout" style="margin:20px 0">In PowerShell, run: <b>.\.venv\Scripts\python.exe src\attendance_app.py</b></div><a class="action" href="http://127.0.0.1:8765/" style="display:inline-block;text-decoration:none">Open live CampusFlow</a></div>';
} else {
  show("overview");
  refresh(true);
  setInterval(() => refresh(false), 5000);
}
