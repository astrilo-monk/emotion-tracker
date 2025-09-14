import cv2
import time
import os
from deepface import DeepFace

# Folder where your images are stored
IMG_FOLDER = "."

# Collect all files that start with "test" and have valid extensions
valid_exts = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
image_files = [f for f in os.listdir(IMG_FOLDER) if f.startswith("test") and f.endswith(valid_exts)]

# Sort them so test1, test2, test3... are in order
image_files.sort()

if not image_files:
    raise FileNotFoundError(" No test images found!")

# Config
DISPLAY_TIME = 5000  # total display time in ms (5 seconds)
STEP = 100           # check for key press every 100 ms

for img_name in image_files:
    img_path = os.path.join(IMG_FOLDER, img_name)
    frame = cv2.imread(img_path)

    if frame is None:
        print(f" Could not read {img_name}, skipping.")
        continue

    # Run DeepFace analysis
    results = DeepFace.analyze(
        img_path=frame,
        actions=['age', 'gender', 'emotion'],
        detector_backend='opencv',
        enforce_detection=False
    )

    if isinstance(results, dict):
        results = [results]

    # Draw results
    for res in results:
        if "region" in res and res["region"]:
            r = res["region"]
            x, y, w, h = r['x'], r['y'], r['w'], r['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            gender = res.get('dominant_gender', '?')
            age = int(res.get('age', 0))
            emotion = res.get('dominant_emotion', '?')
            text = f"{gender} | Age: {age} | {emotion}"

            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2, cv2.LINE_AA)

    # Show result
    cv2.imshow("DeepFace Slideshow", frame)
    print(f"📷 Showing {img_name} for {DISPLAY_TIME/1000:.0f} seconds...")

    # Smarter wait loop: check every 100 ms
    elapsed = 0
    quit_flag = False
    while elapsed < DISPLAY_TIME:
        if cv2.waitKey(STEP) & 0xFF == ord('q'):
            quit_flag = True
            break
        elapsed += STEP

    if quit_flag:
        break

cv2.destroyAllWindows()
