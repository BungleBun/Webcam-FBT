import numpy as np
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#MODEL PATH TO ML MODEL
model_path = 'D:/PythonProjects/Webcam-FBT/pose_landmarker_heavy.task'

#SHORTCUTS FOR TASKS
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

#WEBCAM CAPTURE
cap = cv2.VideoCapture(0)

#PRINTS THE COORDINATES (THIS FUNCTION WILL BE EDITED TO INSTEAD SEND THEM TO THE GAME OSC/DRIVER)
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('pose landmarker result: {}'.format(result))

#SETTINGS AND SPECS FOR THE MODEL
options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_poses=1,
    min_pose_detection_confidence=0.7,
    min_pose_presence_confidence=0.6,
    min_tracking_confidence=0.6,
    output_segmentation_masks=False,
    result_callback=print_result)

with PoseLandmarker.create_from_options(options) as landmarker:
#LOOP TO DISPLAY WEBCAM
    while True:
        ret, frame = cap.read()
        cv2.imshow('Cam1', frame)
        if not ret:
            break

#CONVERT OPENCV'S BGR TO RGB SO THAT MEDIAPIPE CAN READ IT.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

#GENERATE TIMESTAMP
        frame_timestamp_ms = int(time.time() * 1000)

#SENDS DATA TO AI MODEL
        landmarker.detect_async(mp_image, frame_timestamp_ms)

#DISPLAYS TRACKING CAMERA
        cv2.imshow('VR Tracker Feed', frame)

#CLOSES WINDOW IF X KEY PRESSED
        if cv2.waitKey(1) & 0xFF == ord('x'):
            break

#RELEASES WEBCAM TO PREVENT OTHER APPLICATIONS FROM BEING BLOCKED
cap.release()
#FORCE CLOSES ALL WINDOWS
cv2.destroyAllWindows()