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

