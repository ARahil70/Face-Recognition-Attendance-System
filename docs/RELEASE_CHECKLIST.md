# Release checklist

Use this list before publishing the source or proposing campus use.

## Before publishing to GitHub

- [ ] Review the staged and unstaged changes; preserve only intended files.
- [ ] Confirm no face photos, SQLite files, CSV exports, model weights, labels, phone credentials or local settings are being added.
- [ ] Check the full Git history too; **.gitignore** does not remove files from earlier commits.
- [ ] Install from **requirements.txt** in a fresh Python 3.11 environment.
- [ ] Run **python -m compileall -q src** and **node --check src/campusflow/web/app.js**.
- [ ] Start the app and review the dashboard, registration, attendance, exit, reports and Recycle Bin screens.
- [ ] Try the system camera and a phone feed using the phone’s current IP address.
- [ ] Confirm the UI handles an unreachable camera, a blurry face, a duplicate face and the Q cancel key.
- [ ] Test attendance twice for the same person on one date and confirm only one daily entry is stored.
- [ ] Confirm CSV exports have student/faculty separation and the correct course, branch and section.
- [ ] Confirm that restoring a deleted profile preserves its old history and permanent deletion removes it.
- [ ] Choose and add a licence only after confirming project ownership.

## Before official attendance use

- [ ] Get university approval for biometric collection and retention.
- [ ] Add authenticated accounts and role-based permissions.
- [ ] Define a secure central database, encrypted backups and tested recovery.
- [ ] Add a manual correction and non-face attendance route.
- [ ] Assess accuracy and spoofing under actual classrooms, lighting and camera placement.
- [ ] Review the course and branch list with the university.
- [ ] Run a supervised pilot and reconcile records against a trusted manual register.
- [ ] Document who can access, correct, export and permanently delete records.

The current server is local to one computer and has no login. Passing the first list makes the source easier to review; it does not by itself make the system ready for a university-wide deployment.
