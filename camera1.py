import numpy as np
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#CREATE CLIENT FROM CREATE CLIENT FUNCTION
from vrc_osc import create_client
client = create_client()

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

#TRACKING DATA FOR EACH TRACKER
class TrackerData:
    def __init__(self):
        self.left_foot_x = 0.0
        self.left_foot_y = 0.0
        self.left_foot_z = 0.0

        self.right_foot_x = 0.0
        self.right_foot_y = 0.0
        self.right_foot_z = 0.0

        self.left_knee_x = 0.0
        self.left_knee_y = 0.0
        self.left_knee_z = 0.0

        self.right_knee_x = 0.0
        self.right_knee_y = 0.0
        self.right_knee_z = 0.0

        self.hips_x = 0.0
        self.hips_y = 0.0
        self.hips_z = 0.0

        self.chest_x = 0.0
        self.chest_y = 0.0
        self.chest_z = 0.0

        self.left_elbow_x = 0.0
        self.left_elbow_y = 0.0
        self.left_elbow_z = 0.0

        self.right_elbow_x = 0.0
        self.right_elbow_y = 0.0
        self.right_elbow_z = 0.0

#PRINTS THE COORDINATES (THIS FUNCTION WILL BE EDITED TO INSTEAD SEND THEM TO THE GAME OSC/DRIVER)
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    #CANCEL PRINTING FOR NOW TO DECREASE LAG, ONLY USE FOR DEGUBBING
    #print('pose landmarker result: {}'.format(result))
    global client

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
#TRACKER POSITIONS/LANDMARKS
#MAY NEED TO CHANGE FEET TO ANKLE POSITION

        left_foot = landmarks[31]
        right_foot = landmarks[32]
        left_knee = landmarks[25]
        right_knee = landmarks[26]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_chest = landmarks[11]
        right_chest = landmarks[12]
        left_elbow = landmarks[13]
        right_elbow = landmarks[14]

#LANDMARKS USED FOR ROTATION
        left_heel = landmarks[29]
        right_heel = landmarks[30]
        left_ankle = landmarks[27]
        right_ankle = landmarks[28]

#CALCULATES CENTER POINT OF CHEST AND HIP TRACKING
        hips_x = (left_hip.x + right_hip.x) /2
        hips_y = (left_hip.y + right_hip.y) / 2
        hips_z = (left_hip.z + right_hip.z) / 2

        chest_x = (left_chest.x + right_chest.x) / 2
        chest_y = (left_chest.y + right_chest.y) / 2
        chest_z = (left_chest.z + right_chest.z) / 2

#CREATE FORMULA TO CALCULATE FOR ROLL, PITCH, AND YAW BASED ON X Y AND Z COORDINATES

#LEFT FOOT ROTATION FORMULA
        #DIFFERENCE BETWEEN LEFT FOOT AND LEFT HEEL
        dx_left_foot = left_foot.x - left_heel.x
        dy_left_foot = -(left_foot.y - left_heel.y)
        dz_left_foot = left_foot.z - left_heel.z

        #DIFFERENCE BETWEEN LEFT HEEL AND LEFT ANKLE
        dx_left_ankle = left_heel.x - left_ankle.x
        dy_left_ankle = -(left_heel.y - left_ankle.y)
        dz_left_ankle = left_heel.z - left_ankle.z

        #FLOOR LENGTH DISTANCE BETWEEN HEEL AND TOE
        left_foot_floor_length = np.sqrt(dx_left_foot ** 2 + dz_left_foot ** 2)

        #DISTANCE BETWEEN HEEL AND ANKLE (MAYBE OBSOLETE CODE BUT KEEP JUST IN CASE TESTING NEEDS IT)
        #ankle_vert_dist = np.sqrt(dx_left_ankle ** 2 + dz_left_ankle ** 2)

        #CALCULATES FOR BODY ROTATION FOR CLEAN ROLL
        side_shift_lf = (dx_left_ankle * dx_left_foot) + (dz_left_ankle * dz_left_foot)

        #FOOT ROTATION
        left_foot_pitch = np.degrees(np.arctan2(dy_left_foot, left_foot_floor_length))
        left_foot_yaw = np.degrees(np.arctan2(dx_left_foot, dz_left_foot))
        left_foot_roll = np.degrees(np.arctan2(side_shift_lf, dy_left_ankle))

# RIGHT FOOT ROTATION FORMULA
        # DIFFERENCE BETWEEN RIGHT FOOT AND RIGHT HEEL
        dx_right_foot = right_foot.x - right_heel.x
        dy_right_foot = -(right_foot.y - right_heel.y)
        dz_right_foot = right_foot.z - right_heel.z

        # DIFFERENCE BETWEEN LEFT HEEL AND LEFT ANKLE
        dx_right_ankle = right_heel.x - right_ankle.x
        dy_right_ankle = -(right_heel.y - right_ankle.y)
        dz_right_ankle = right_heel.z - right_ankle.z

        # FLOOR LENGTH DISTANCE BETWEEN HEEL AND TOE
        right_foot_floor_length = np.sqrt(dx_right_foot ** 2 + dz_right_foot ** 2)

        # DISTANCE BETWEEN HEEL AND ANKLE (MAYBE OBSOLETE CODE BUT KEEP JUST IN CASE TESTING NEEDS IT)
        # ankle_vert_dist = np.sqrt(dx_right_ankle ** 2 + dz_right_ankle ** 2)

        # CALCULATES FOR BODY ROTATION FOR CLEAN ROLL
        side_shift_rf = (dx_right_ankle * dx_right_foot) + (dz_right_ankle * dz_right_foot)

        #FOOT ROTATION
        right_foot_pitch = np.degrees(np.arctan2(dy_right_foot, right_foot_floor_length))
        right_foot_yaw = np.degrees(np.arctan2(dx_right_foot, dz_right_foot))
        right_foot_roll = np.degrees(np.arctan2(side_shift_rf, dy_right_ankle))

# LEFT KNEE ROTATION FORMULA
        #DIFFERENCE BETWEEN LEFT KNEE AND LEFT HIP
        dx_left_thigh = left_knee.x - left_hip.x
        dy_left_thigh = -(left_knee.y - left_hip.y)
        dz_left_thigh = left_knee.z - left_hip.z

        #DIFFERENCE BETWEEN LEFT KNEE AND LEFT ANKLE
        dx_left_shin = left_ankle.x - left_knee.x
        dy_left_shin = -(left_ankle.y - left_knee.y)
        dz_left_shin = left_ankle.z - left_knee.z

        #FLOOR LANGTH BETWEEN THIGH
        left_thigh_floor_length = np.sqrt(dx_left_thigh**2 + dz_left_thigh**2)

        #TRACK FOR KNEE ROTATION
        left_knee_side_shift = (dx_left_thigh * dx_left_foot) + (dz_left_thigh * dz_left_foot)

        #KNEE ROTATION
        left_knee_pitch = np.degrees(np.arctan2(dy_left_thigh, left_thigh_floor_length))
        left_knee_yaw = left_foot_yaw
        left_knee_roll = np.degrees(np.arctan2(left_knee_side_shift, dy_left_thigh))

# RIGHT KNEE ROTATION FORMULA
        # DIFFERENCE BETWEEN RIGHT KNEE AND RIGHT HIP
        dx_right_thigh = right_knee.x - right_hip.x
        dy_right_thigh = -(right_knee.y - right_hip.y)
        dz_right_thigh = right_knee.z - right_hip.z

        # DIFFERENCE BETWEEN RIGHT KNEE AND RIGHT ANKLE
        dx_right_shin = right_ankle.x - right_knee.x
        dy_right_shin = -(right_ankle.y - right_knee.y)
        dz_right_shin = right_ankle.z - right_knee.z

        # FLOOR LANGTH BETWEEN THIGH
        right_thigh_floor_length = np.sqrt(dx_right_thigh ** 2 + dz_right_thigh ** 2)

        # TRACK FOR KNEE ROTATION
        right_knee_side_shift = (dx_right_thigh * dx_right_foot) + (dz_right_thigh * dz_right_foot)

        # KNEE ROTATION
        right_knee_pitch = np.degrees(np.arctan2(dy_right_thigh, right_thigh_floor_length))
        right_knee_yaw = right_foot_yaw
        right_knee_roll = np.degrees(np.arctan2(right_knee_side_shift, dy_right_thigh))
# HIPS ROTATION FORMULA
        #DIFFERENCE BETWEEN LEFT HIP AND RIGHT HIP
        dx_pelvis = left_hip.x - right_hip.x
        dy_pelvis = -(left_hip.y - right_hip.y)
        dz_pelvis = left_hip.z - right_hip.z

        #DIFFERENCE BETWEEN HIPS AND CHEST
        dx_hips_spine = chest_x - hips_x
        dy_hips_spine = -(chest_y - hips_y)
        dz_hips_spine = chest_z - hips_z

        #FLOOR LENGTH BETWEEN SPINE
        hips_spine_floor_length = np.sqrt(dx_hips_spine ** 2 + dz_hips_spine ** 2)

        #TRACK FOR PELVIS WIDTH
        pelvis_width = np.sqrt(dx_pelvis ** 2 + dz_pelvis ** 2)

        #HIP ROTATION
        hips_pitch = np.degrees(np.arctan2(dy_hips_spine, hips_spine_floor_length))
        hips_yaw = np.degrees(np.arctan2(dz_pelvis, dx_pelvis))
        hips_roll = np.degrees(np.arctan2(dy_pelvis, pelvis_width))

# CHEST ROTATION FORMULA
        #DIFFERENCE BETWEEN CHEST
        dx_chest = left_chest.x - right_chest.x
        dy_chest = -(left_chest.y - right_chest.y)
        dz_chest = left_chest.z - right_chest.z

        #DIFFERENCE BETWEEN CHEST AND HIPS
        dx_chest_spine = chest_x - hips_x
        dy_chest_spine = -(chest_y - hips_y)
        dz_chest_spine = chest_z - hips_z

        #FLOOR LENGTH BETWEEN SPINE
        chest_spine_floor_length = np.sqrt(dx_chest_spine ** 2 + dz_chest_spine ** 2)

        #TRACK FOR CHEST WIDTH
        chest_width = np.sqrt(dx_chest ** 2 + dz_chest ** 2)

        #CHEST ROTATION
        chest_pitch = np.degrees(np.arctan2(dy_chest_spine, chest_spine_floor_length))
        chest_yaw = np.degrees(np.arctan2(dy_chest, chest_width))
        chest_roll = np.degrees(np.arctan2(dz_chest, dx_chest))

#LEFT ELBOW ROTATION FORMULA
        #DIFFERENCE BETWEEN CHEST AND ELBOW
        dx_left_bicep = left_elbow.x - left_chest.x
        dy_left_bicep = -(left_elbow.y - left_chest.y)
        dz_left_bicep = left_elbow.z - left_chest.z

        #I THINK I CAN GET AWAY WITH JUST LETTING VRCHAT'S ENGINE TAKE OVER THE YAW AND ROLL BY MATCHING TO THE PLAYER'S CONTROLLER

        #FLOOR LENGTH BETWEEN BICEP
        bicep_floor_length = np.sqrt(dx_left_bicep ** 2 + dz_left_bicep ** 2)

        left_elbow_pitch = np.degrees(np.arctan2(dy_left_bicep, bicep_floor_length))
        left_elbow_yaw = 0.0
        left_elbow_roll = 0.0

# RIGHT ELBOW ROTATION FORMULA
        # DIFFERENCE BETWEEN CHEST AND ELBOW
        dx_right_bicep = right_elbow.x - right_chest.x
        dy_right_bicep = -(right_elbow.y - right_chest.y)
        dz_right_bicep = right_elbow.z - right_chest.z

        # I THINK I CAN GET AWAY WITH JUST LETTING VRCHAT'S ENGINE TAKE OVER THE YAW AND ROLL BY MATCHING TO THE PLAYER'S CONTROLLER

        # FLOOR LENGTH BETWEEN BICEP
        bicep_floor_length = np.sqrt(dx_right_bicep ** 2 + dz_right_bicep ** 2)

        right_elbow_pitch = np.degrees(np.arctan2(dy_right_bicep, bicep_floor_length))
        right_elbow_yaw = 0.0
        right_elbow_roll = 0.0

#SENDS POSITION DATA TO VRCHAT OSC
        client.send_message("/tracking/trackers/1/position",
                            [left_foot.x, left_foot.y, left_foot.z])  # Position
        client.send_message("/tracking/trackers/1/rotation",
                            [left_foot_pitch, left_foot_yaw, left_foot_roll])  # Rotation
        client.send_message("/tracking/trackers/2/position",
                            [right_foot.x, right_foot.y, right_foot.z])  # Position
        client.send_message("/tracking/trackers/2/rotation",
                            [right_foot_pitch, right_foot_yaw, right_foot_roll])  # Rotation
        client.send_message("/tracking/trackers/3/position",
                            [left_knee.x, left_knee.y, left_knee.z])  # Position
        client.send_message("/tracking/trackers/3/rotation",
                            [left_knee_pitch, left_knee_yaw, left_knee_roll])  # Rotation
        client.send_message("/tracking/trackers/4/position",
                            [right_knee.x, right_knee.y, right_knee.z])  # Position
        client.send_message("/tracking/trackers/4/rotation",
                            [right_knee_pitch, right_knee_yaw, right_knee_roll])  # Rotation
        client.send_message("/tracking/trackers/5/position", [hips_x, hips_y, hips_z])  # Position
        client.send_message("/tracking/trackers/5/rotation",
                            [hips_pitch, hips_yaw, hips_roll])  # Rotation
        client.send_message("/tracking/trackers/6/position",
                            [chest_x, chest_y, chest_z])  # Position
        client.send_message("/tracking/trackers/6/rotation",
                            [chest_pitch, chest_yaw, chest_roll])  # Rotation
        client.send_message("/tracking/trackers/7/position",
                            [left_elbow.x, left_elbow.y, left_elbow.z])  # Position
        client.send_message("/tracking/trackers/7/rotation",
                            [left_elbow_pitch, left_elbow_yaw, left_elbow_roll])  # Rotation
        client.send_message("/tracking/trackers/8/position",
                            [right_elbow.x, right_elbow.y, right_elbow.z])  # Position
        client.send_message("/tracking/trackers/8/rotation",
                            [right_elbow_pitch, right_elbow_yaw, right_elbow_roll])  # Rotation

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