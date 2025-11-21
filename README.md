#  Emotion Tracker

A full facial analysis system using DeepFace for detecting emotion, age, and gender.  
Includes real-time webcam processing, static image batch analysis, and a web-based interface.

---

## Overview

This project provides three modes of operation:

1. **Real-Time Analysis (`main.py`)**  
   High-performance webcam analysis with multithreading for smoother FPS and non-blocking frame capture.

2. **Static Image Analysis (`v2/v2.py`)**  
   Processes a folder of test images (e.g., test1.jpg, test2.jpg) and displays results in a slideshow format.

3. **Web Interface (`app.py`)**  
   A Flask-based UI for uploading images through the browser and receiving age, gender, and emotion results.

---

## Features

### Real-Time Mode (`main.py`)
- Multithreaded architecture to separate capture, analysis, and display.
- Stable FPS even when DeepFace analysis is slow.
- Selfie-mode camera mirroring.
- Fallback face detection using OpenCV Haar Cascade.
- Configurable camera index, analysis frequency, and resolution.

### Static Image Mode (`v2/v2.py`)
- Scans a folder for files named `test1.jpg`, `test2.jpg`, etc.
- Runs DeepFace analysis on each image.
- Displays results in a timed slideshow window.

### Web Interface (`app.py`)
- Upload an image through a browser.
- Backend runs DeepFace analysis and returns a clean JSON response.
- Frontend displays emotion, age, and gender in a styled UI.
- Fully self-contained (HTML served from Flask).

---

## Installation

Clone the repository:

```
git clone https://github.com/astrilo-monk/emotion-tracker.git
cd emotion-tracker
```

It is recommended to use a virtual environment:

```
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

Install required libraries:

```
pip install -r requirements.txt
```

If you prefer installing manually (local setup):

```
1. pip install opencv-python deepface
2. pip install tensorflow
3. pip install tensorflow[and-cuda]     (optional, GPU users only)
4. pip install mtcnn retina-face mediapipe   (optional detectors)
5. pip install flask gunicorn numpy         (web interface)
```

---

## Running the Web Interface

Start the Flask server:

```
python app.py
```

Visit the web UI:

```
http://127.0.0.1:5000/
```

Upload an image and view the results directly in the browser.

Video showcasing the website:: 
https://github.com/user-attachments/assets/0d5a6d3f-df59-44a0-8ee0-6f5e51be8c1a

## Running Real-Time Webcam Mode

```
python main.py
```

This opens a live webcam window with continuously updated results.

---

## Running Static Image Mode

Place test images inside the `v2/` folder with names like:

```
test1.jpg
test2.jpg
test3.jpg
```

Then run:

```
python v2/v2.py
```

---

## Project Structure

```
emotion-tracker/
│
├── app.py                # Web backend (Flask)
├── main.py               # Real-time webcam analyzer
├── requirements.txt      
├── README.md
│
├── templates/
│   └── index.html        # Web UI
│
└── v2/
    ├── v2.py             # Static image analyzer
    ├── test1.jpg
    ├── test2.jpg
    ├── ...
```

---

## Notes

- First DeepFace analysis may take time due to model loading.
- For deployment, a long-running Python environment is required (Render recommended).
- GPU acceleration is optional but provides faster inference if supported.

---


