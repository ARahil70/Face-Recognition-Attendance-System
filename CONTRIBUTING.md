# Contributing

Thanks for helping improve CampusFlow. Keep changes small enough to review and describe what changed and how it was checked.

## Before opening a pull request

- Do not include real face samples, student or faculty records, database files, exports, model weights or credentials.
- Keep the browser dashboard as the supported interface unless the change explicitly updates the launcher and documentation.
- Update the setup or privacy notes whenever a change affects stored data, camera access or installation.
- Use four spaces in Python and two spaces in HTML, CSS and JavaScript.
- Include a screenshot or short reproduction note for visible UI changes. Use fictional sample data.

## Local checks

~~~powershell
.\.venv\Scripts\python.exe -m compileall -q src
node --check src\campusflow\web\app.js
~~~

The current CI job checks source syntax. It does not run a face-recognition accuracy test or a full camera integration test.
