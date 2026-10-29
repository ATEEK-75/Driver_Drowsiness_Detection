# Driver Drowsiness Detection — OpenCV + ML

A learning project that uses a webcam, OpenCV, MediaPipe Face Mesh, and Eye Aspect Ratio (EAR) to flag prolonged eye closure and play an alert.

## Features
- Live webcam feed
- Facial eye landmark visualization
- Eye Aspect Ratio (EAR) display
- Alert when eyes appear closed for a configured duration
- Keyboard shortcut `Q` or `Esc` to exit
- Auto-compatible with Python 3.11, 3.12, and 3.13+ (supports both modern MediaPipe Tasks API and legacy solutions API)

## Requirements
- Windows/macOS/Linux
- Python 3.11, 3.12, or 3.13
- Working webcam

## Setup (Windows)
1. Double-click `run_windows.bat`, or run these commands in your terminal:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

## Controls
- Press `Q` or `Esc` in the webcam window to stop.

## How it works
1. MediaPipe detects facial landmarks (using modern `FaceLandmarker` or legacy `mp.solutions.face_mesh`).
2. Six landmarks around each eye are used to calculate the Eye Aspect Ratio (EAR).
3. If the average EAR stays below `EAR_THRESHOLD` for `CLOSED_SECONDS`, the program displays a drowsiness warning and plays a beep.

Tune `EAR_THRESHOLD` and `CLOSED_SECONDS` near the top of `app.py` for experimentation. Thresholds vary with camera angle, lighting, face shape, and glasses.

## Troubleshooting
- **Camera won't open:** close Zoom/Teams/Camera app and retry; check Windows camera permissions.
- **Dependency installation fails:** ensure you are using 64-bit Python and that pip is up to date (`python -m pip install --upgrade pip`).
- **No beep:** the video warning still works; check system volume.

## Important safety note
This is an educational prototype, not a validated or certified driver-monitoring system. It can miss drowsiness or trigger false alarms. Do not rely on it to make driving safe, and never test it while driving.
