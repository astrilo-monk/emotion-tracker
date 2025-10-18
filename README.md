# Optimized DeepFace Analysis (Real-Time and Static)

This project provides two Python scripts for face analysis (age, gender, emotion) using the `DeepFace` library, with a focus on performance and usability.

1.  **`realtime_deepface_fast_inverted.py`**: A high-performance, multithreaded script for real-time webcam analysis.
2.  **`analyze_static_images.py`**: A simple script to analyze a folder of static images (e.g., `test1.jpg`, `test2.jpg`) and display them as a slideshow.

---

## Features

* **High-FPS Real-Time Analysis**: The webcam script uses a multithreaded, queued architecture to achieve a smooth display framerate, independent of the analysis speed.
* **Decoupled Analysis**: A dedicated worker thread handles the slow `DeepFace.analyze()` calls, so it doesn't block the main display loop.
* **Non-Blocking Camera Feed**: A capture thread reads from the webcam, preventing I/O lag.
* **Mirrored "Selfie" Mode**: The webcam feed is horizontally flipped for a more intuitive, natural-feeling display.
* **Robust Fallback**: If `DeepFace` fails to find a face, the script falls back to a faster OpenCV Haar Cascade detector to at least draw a box.
* **Configurable**: Easily change camera index, analysis frequency, and resize dimensions in the `CONFIG` block of the real-time script.

---

## How the High-FPS Optimization Works

The core problem with real-time analysis is that `DeepFace.analyze()` is **slow** (it runs a deep learning model) and `cv2.VideoCapture.read()` can be a **blocking I/O call**. Performing both in a single loop results in a laggy, low-FPS video stream.

This script solves the problem by using **three parallel threads**:

1.  **`VideoCaptureThread` (Capture Thread)**
    * **Job**: Its *only* job is to constantly read frames from the webcam.
    * **Queue**: It puts the latest frame into a small queue (`self.q`), overwriting old frames.
    * **Benefit**: The main thread can grab the most recent frame from this queue *instantly* without waiting for the camera.

2.  **`analysis_worker` (Worker Thread)**
    * **Job**: Its *only* job is to perform the slow `DeepFace.analyze()` task.
    * **Queues**: It waits for a frame to appear in an *input queue* (`in_q`), analyzes it, and puts the JSON *result* into an *output queue* (`out_q`).
    * **Benefit**: The slow analysis happens on a separate core and does not block the display.

3.  **`main` (Main/Display Thread)**
    * **Job**: Runs the main `while True` loop as fast as possible to render the video.
    * **Loop**:
        1.  **Get Frame**: Instantly grabs the latest frame from the `VideoCaptureThread`'s queue.
        2.  **Check for Result**: *Checks* (doesn't wait) if a new result is available in the `out_q` from the worker. If yes, it updates `last_result`.
        3.  **Draw**: Draws the `last_result` (the most recent analysis data) onto the *current* frame.
        4.  **Send Frame**: Every `N` frames, it sends a copy of the current frame to the `in_q` for the worker to analyze.

This architecture **decouples** the display FPS from the analysis FPS. You get a smooth 30-60 FPS video feed, even if the analysis only runs 5-10 times per second.

---

## Installation

1.  Clone this repository:
    ```bash
    # Replace 'your-repo-name' with the name of your actual repository
    git clone [https://github.com/astrio-monk/your-repo-name.git](https://github.com/astrio-monk/your-repo-name.git)
    cd your-repo-name
    ```

2.  Install the required Python libraries. It's highly recommended to use a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

    A `requirements.txt` file should contain:
    ```
    opencv-python
    deepface
    ```

---

