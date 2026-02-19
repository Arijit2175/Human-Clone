import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

hands = mp_hands.Hands(max_num_hands=2)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("Mirror Humanoid Clone", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Mirror Humanoid Clone", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

alpha = 0.7      
smoothed_pts = None 

X_OFFSET = 250
Y_OFFSET = -60

BODY_COLOR = (139, 0, 0)    
HAND_COLOR = (0, 140, 255)  
HEAD_COLOR = (0, 0, 255)     

def smooth_points(old, new):
    if old is None:
        return new
    out = {}
    for k in new:
        ox, oy = old.get(k, new[k])
        nx, ny = new[k]
        sx = ox * alpha + nx * (1 - alpha)
        sy = oy * alpha + ny * (1 - alpha)
        out[k] = (int(sx), int(sy))
    return out

def extract_pose_points(results, w, h):
    pts = {}
    if results.pose_landmarks:
        for i, lm in enumerate(results.pose_landmarks.landmark):
            x = int((1 - lm.x) * w) + X_OFFSET
            y = int(lm.y * h) + Y_OFFSET
            pts[i] = (x, y)
    return pts

def extract_hand_points(results, w, h):
    hands_pts = []
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            pts = []
            for lm in hand.landmark:
                x = int((1 - lm.x) * w) + X_OFFSET
                y = int(lm.y * h) + Y_OFFSET
                pts.append((x, y))
            hands_pts.append(pts)
    return hands_pts

