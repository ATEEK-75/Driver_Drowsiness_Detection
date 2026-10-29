"""
Driver Drowsiness Detection — educational webcam prototype
Uses MediaPipe Face Mesh eye landmarks + Eye Aspect Ratio (EAR).
This is NOT a certified vehicle safety system.
"""
import os
import sys
import time
import threading
import urllib.request

import cv2
import numpy as np
import mediapipe as mp

try:
    import winsound
except ImportError:
    winsound = None

# Face Mesh landmark indices (MediaPipe Face Mesh)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

EAR_THRESHOLD = 0.21
CLOSED_SECONDS = 1.5
CAMERA_INDEX = 0

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
MODEL_FILENAME = "face_landmarker.task"


class FaceLandmarkDetector:
    """Unified detector supporting both modern MediaPipe Tasks API and legacy solutions API."""

    def __init__(self):
        self.use_tasks_api = False
        self.detector = None

        if hasattr(mp, "solutions") and hasattr(mp.solutions, "face_mesh"):
            # Legacy MediaPipe solutions API
            self.detector = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
        else:
            # Modern MediaPipe tasks API (MediaPipe >= 0.10.14 / 1.0+)
            self.use_tasks_api = True
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_FILENAME)
            if not os.path.exists(model_path):
                print(f"Downloading MediaPipe Face Landmarker model to {model_path}...")
                try:
                    urllib.request.urlretrieve(MODEL_URL, model_path)
                    print("Download complete.")
                except Exception as exc:
                    print(f"Failed to auto-download model file: {exc}")
                    raise

            from mediapipe.tasks.python import vision, BaseOptions

            options = vision.FaceLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=model_path),
                running_mode=vision.RunningMode.IMAGE,
                num_faces=1,
                min_face_detection_confidence=0.5,
                min_face_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            self.detector = vision.FaceLandmarker.create_from_options(options)

    def process(self, frame_bgr):
        """Processes a BGR image frame and returns landmarks for the first detected face."""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        if self.use_tasks_api:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
            result = self.detector.detect(mp_image)
            if result.face_landmarks and len(result.face_landmarks) > 0:
                return result.face_landmarks[0]
            return None
        else:
            results = self.detector.process(frame_rgb)
            if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
                return results.multi_face_landmarks[0].landmark
            return None

    def close(self):
        if hasattr(self.detector, "close"):
            self.detector.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def open_camera(camera_index):
    """Open camera with DirectShow backend first on Windows for fast startup, then fallback."""
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
    return cv2.VideoCapture(camera_index)


def eye_aspect_ratio(landmarks, eye_indices, width, height):
    """Calculate Eye Aspect Ratio (EAR) from six eye landmarks."""
    points = []
    for idx in eye_indices:
        lm = landmarks[idx]
        points.append(np.array([lm.x * width, lm.y * height], dtype=np.float32))

    # Vertical distances / (2 * horizontal distance)
    vertical_1 = np.linalg.norm(points[1] - points[5])
    vertical_2 = np.linalg.norm(points[2] - points[4])
    horizontal = np.linalg.norm(points[0] - points[3])

    if horizontal == 0:
        return 0.0
    return float((vertical_1 + vertical_2) / (2.0 * horizontal))


def play_alert():
    """Play a short alert without blocking the video loop."""
    if winsound:
        try:
            winsound.Beep(1400, 350)
        except Exception:
            pass
    else:
        print("\a", end="", flush=True)


def main():
    camera = open_camera(CAMERA_INDEX)

    if not camera.isOpened():
        print("ERROR: Webcam open nahi ho raha. Camera permission/check kijiye.")
        return

    closed_start = None
    last_alert_time = 0.0

    print("Driver Drowsiness Detection started. Exit ke liye Q dabayein.")
    with FaceLandmarkDetector() as face_mesh:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("ERROR: Webcam se frame nahi mil raha.")
                break

            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]
            landmarks = face_mesh.process(frame)

            status = "NO FACE DETECTED"
            color = (0, 200, 255)

            if landmarks is not None:
                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, width, height)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, width, height)
                ear = (left_ear + right_ear) / 2.0

                # Draw eye landmark points for visual feedback.
                for idx in LEFT_EYE + RIGHT_EYE:
                    lm = landmarks[idx]
                    px, py = int(lm.x * width), int(lm.y * height)
                    cv2.circle(frame, (px, py), 2, (255, 200, 0), -1)

                cv2.putText(frame, f"EAR: {ear:.3f}", (20, 75),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                if ear < EAR_THRESHOLD:
                    if closed_start is None:
                        closed_start = time.monotonic()
                    closed_duration = time.monotonic() - closed_start

                    if closed_duration >= CLOSED_SECONDS:
                        status = "DROWSINESS DETECTED!"
                        color = (0, 0, 255)
                        if time.monotonic() - last_alert_time > 2.0:
                            threading.Thread(target=play_alert, daemon=True).start()
                            last_alert_time = time.monotonic()
                    else:
                        status = "EYES CLOSED"
                        color = (0, 165, 255)
                else:
                    closed_start = None
                    status = "ALERT - EYES OPEN"
                    color = (0, 200, 0)

            cv2.rectangle(frame, (10, 15), (width - 10, 52), (25, 25, 25), -1)
            cv2.putText(frame, status, (20, 42),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
            cv2.putText(frame, "Q: Quit | Educational prototype only", (20, height - 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1)

            cv2.imshow("Driver Drowsiness Detection", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
