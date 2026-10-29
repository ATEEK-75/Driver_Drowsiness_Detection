# Driver Drowsiness Detection

## Project Overview

Driver Drowsiness Detection is a computer vision project designed to identify signs of driver fatigue by monitoring eye activity through a camera.

The system processes live camera frames using Python and OpenCV and detects whether the driver's eyes are open or closed. It can help demonstrate how computer vision can be applied to road safety.

## Objectives

* Monitor eye activity using a camera.
* Detect eye-open and eye-closed states.
* Identify potential signs of drowsiness.
* Explore real-time computer vision applications.
* Develop a practical project using Python.

## Features

* Real-time camera input.
* Eye activity monitoring.
* Eye Open and Eye Closed status detection.
* Visual feedback based on detected eye activity.
* Python-based implementation.
* Computer vision processing using OpenCV.

*Note: Features depend on the implementation in the uploaded source code.*

## Technologies Used

* Python
* OpenCV
* Computer Vision
* MediaPipe, if used in the project code
* Machine Learning, if implemented in the project code

## Project Workflow

1. Initialize the camera.
2. Capture video frames.
3. Process frames using computer vision techniques.
4. Detect facial or eye-related landmarks, if supported by the implementation.
5. Determine the eye state using the implemented detection method.
6. Display the detection result on the screen.
7. Generate a warning if the project's implemented logic detects prolonged eye closure.

## Project Structure

The repository may contain the following files:

```text
Driver_Drowsiness_Detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    └── screenshots/
```

Keep only the files and folders that actually exist in your project. Add any training scripts, model files, or additional resources that your implementation requires.

## Requirements

* Python 3.x
* A working webcam
* pip
* Required Python libraries

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Driver_Drowsiness_Detection.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project Folder

```bash
cd Driver_Drowsiness_Detection
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

If the file is not available, install the dependencies required by your actual source code.

For example:

```bash
pip install opencv-python
```

Install MediaPipe or other packages only if your code uses them.

### 5. Run the Project

```bash
python app.py
```

Allow camera access if prompted.

## Expected Output

When the application runs successfully, the camera feed should appear and the program should display the eye-state information supported by the implementation.

If prolonged eye closure detection and alerts are implemented, the application may also display a warning when its detection conditions are met.

## Applications

* Computer vision learning.
* Driver safety research prototypes.
* Real-time image processing demonstrations.
* Academic projects and practical learning.

## Limitations

* Detection performance depends on camera quality and lighting.
* Glasses, head movement, and camera position may affect results.
* Eye-state detection alone cannot reliably establish whether a driver is drowsy.
* The project is an educational prototype and is not a certified vehicle safety system.

## Future Improvements

* Improve detection accuracy under different lighting conditions.
* Add reliable drowsiness-duration analysis.
* Integrate audio alerts.
* Evaluate performance on a representative dataset.
* Improve robustness against head movement and partial facial occlusion.

## Author

**Ateek Ahamad**

B.Tech CSE (Artificial Intelligence and Machine Learning)

## Disclaimer

This project is intended for educational and demonstration purposes only. It must not be relied upon as the sole method of detecting driver fatigue or preventing road accidents.
