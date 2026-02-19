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

def draw_limb(img, p1, p2, color, thickness):
    cv2.line(img, p1, p2, color, thickness, cv2.LINE_AA)
    cv2.circle(img, p1, thickness//2, color, -1, cv2.LINE_AA)
    cv2.circle(img, p2, thickness//2, color, -1, cv2.LINE_AA)

def draw_hand(img, pts):
    connections = mp_hands.HAND_CONNECTIONS

    for a, b in connections:
        cv2.line(img, pts[a], pts[b], HAND_COLOR, 16, cv2.LINE_AA)
    for p in pts:
        cv2.circle(img, p, 10, HAND_COLOR, -1, cv2.LINE_AA)

    for a, b in connections:
        cv2.line(img, pts[a], pts[b], HAND_COLOR, 8, cv2.LINE_AA)
    for p in pts:
        cv2.circle(img, p, 5, HAND_COLOR, -1, cv2.LINE_AA)

def draw_humanoid(img, pts, hands_pts):
    if not pts:
        return

    P = mp_pose.PoseLandmark

    limbs = [
        (P.LEFT_SHOULDER.value, P.LEFT_ELBOW.value),
        (P.LEFT_ELBOW.value, P.LEFT_WRIST.value),
        (P.RIGHT_SHOULDER.value, P.RIGHT_ELBOW.value),
        (P.RIGHT_ELBOW.value, P.RIGHT_WRIST.value),
        (P.LEFT_HIP.value, P.LEFT_KNEE.value),
        (P.LEFT_KNEE.value, P.LEFT_ANKLE.value),
        (P.RIGHT_HIP.value, P.RIGHT_KNEE.value),
        (P.RIGHT_KNEE.value, P.RIGHT_ANKLE.value),
    ]

    for a, b in limbs:
        if a in pts and b in pts:
            draw_limb(img, pts[a], pts[b], BODY_COLOR, 20)

    if all(k in pts for k in [
        P.LEFT_SHOULDER.value, P.RIGHT_SHOULDER.value,
        P.LEFT_HIP.value, P.RIGHT_HIP.value
    ]):
        torso = np.array([
            pts[P.LEFT_SHOULDER.value],
            pts[P.RIGHT_SHOULDER.value],
            pts[P.RIGHT_HIP.value],
            pts[P.LEFT_HIP.value]
        ])
        cv2.fillPoly(img, [torso], BODY_COLOR)

    if P.NOSE.value in pts:
        cv2.circle(img, pts[P.NOSE.value], 90, HEAD_COLOR, -1, cv2.LINE_AA)

    for hand in hands_pts:
        draw_hand(img, hand)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_results = pose.process(rgb)
    hand_results = hands.process(rgb)

    pts = extract_pose_points(pose_results, w, h)
    hands_pts = extract_hand_points(hand_results, w, h)

    smoothed_pts = smooth_points(smoothed_pts, pts)

    draw_humanoid(frame, smoothed_pts, hands_pts)

    cv2.imshow("Mirror Humanoid Clone", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

