# 🪞 Mirror Humanoid Clone

A real-time humanoid mirror clone built with OpenCV and MediaPipe.
It tracks your body and hands using your webcam and draws a stylized humanoid figure that mimics your movement, with glowing hands and a solid-colored body.

---

## ✨ Features

- Real-time body pose tracking (head, arms, legs, torso)

- Real-time hand tracking (fingers included)

- Glowing, thick hand and finger effect

- Smooth motion using point interpolation

- Fullscreen 1920×1080 display

- Mirrored movement (acts like a mirror)

- Stylized humanoid rendering (no camera feed replacement, only overlay)

---

## 🛠️ Tech Stack

| Technology | Version |
|------------|---------|
| Python     | 3.9 or 3.10 |
| OpenCV     | 4.8.0.76 |
| MediaPipe  | 0.10.9 |
| NumPy      | 1.24.4 |

> ⚠️ MediaPipe is NOT stable on Python 3.11+.  
> Use Python 3.9 or 3.10 to avoid installation and runtime issues.

---

## 📁 Project Structure

```
clone.py
README.md
```

---

## 📦 Installation and Execution

### 1. Create Virtual Environment (Recommended)

```
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```
pip install opencv-python==4.8.0.76 mediapipe==0.10.9 numpy==1.24.4
```

### ▶️ Run the Project

```
python clone.py
```

Press ESC to exit.

---

## 🧠 How It Works

- MediaPipe Pose tracks body landmarks.
- MediaPipe Hands tracks finger joints.
- Coordinates are flipped horizontally for mirror effect.
- A humanoid stickman is drawn using OpenCV primitives.
- A smoothing filter blends frames to reduce jitter.
- Hands are drawn thicker for a glowing effect.

---

## 🖥️ Output

- Fullscreen webcam window
- Clone appears beside you

---

## 📚 References

- MediaPipe Pose Documentation  
  https://developers.google.com/mediapipe/solutions/vision/pose

- MediaPipe Hands Documentation  
  https://developers.google.com/mediapipe/solutions/vision/hand_landmarker

- OpenCV Python Documentation  
  https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

- NumPy Documentation  
  https://numpy.org/doc/

- Python Official Documentation  
  https://docs.python.org/3/

- Real-Time Pose Tracking Paper  
  Lugaresi et al., "MediaPipe: A Framework for Building Perception Pipelines", Google AI, 2019.

<br>

👨‍💻 **Developed by** – @Arijit2175