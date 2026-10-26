# Windows setup

## Requirements

- Windows 10 or 11, 64-bit.
- Python 3.11, 64-bit.
- A system camera, or an Android phone running IP Webcam on the same Wi-Fi.
- Internet access for the first package installation.

TensorFlow uses the CPU on native Windows in this project. The official TensorFlow guide documents the supported Windows install and the native-Windows GPU limit: https://www.tensorflow.org/install/pip.

## Install

Open PowerShell in the project folder:

~~~powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
~~~

Then start the app:

~~~powershell
.\.venv\Scripts\python.exe src\attendance_app.py
~~~

Keep that process open. The dashboard uses http://127.0.0.1:8765. If that address is already in use, close the other CampusFlow process first.

## First-time setup

1. Register at least two people. Training starts automatically after the second profile has been saved.
2. Wait for the model status to show that it is up to date before starting attendance or exit scans.
3. Start a camera scan from its own page. Press **Q** in the camera window or use **Stop scan** in the dashboard.
4. Check the Records & reports page and confirm the name, role, date and course details before relying on an export.

The model and face samples are created on this computer; they are not supplied in the repository.

## IP Webcam

1. Start the IP Webcam server on the phone.
2. Put the phone and computer on the same Wi-Fi network.
3. Enter the current base address shown by the phone, for example http://192.168.1.25:8080. CampusFlow appends /shot.jpg. A full /shot.jpg address and a /video address are also accepted.
4. On the computer, open http://192.168.1.25:8080/shot.jpg in a browser. Continue only if an image appears.
5. Keep the phone screen awake and the IP Webcam server running while capturing or scanning.

The address in this example is only a sample. Use the address shown by your phone each time; routers can assign a different IP after reconnecting.

## Start at Windows sign-in

This is optional. The task runs under the current Windows user and opens the local dashboard at sign-in.

~~~powershell
powershell -ExecutionPolicy Bypass -File .\install_autostart.ps1
~~~

Remove it with:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\remove_autostart.ps1
~~~

## Back up local records

The Recycle Bin can restore profiles removed inside the app, but it cannot recover from a damaged or lost drive. Stop CampusFlow, then copy the entire **data** folder to storage approved by the university. Keep the backup private because it contains biometric samples and attendance history. The model files can be recreated from the saved samples.
