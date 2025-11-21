from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import cv2
import numpy as np

app = Flask(__name__)

def analyze_uploaded_image(image_bytes):
    # convert bytes -> OpenCV image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        print("❌ cv2 could not decode image")
        raise ValueError("Invalid image data")

    print("🖼 image decoded, shape:", img.shape)

    # run DeepFace
    result = DeepFace.analyze(
        img_path=img,
        actions=["emotion", "age", "gender"],
        detector_backend="opencv",
        enforce_detection=False
    )

    print("✅ DeepFace.analyze returned")

    # sometimes DeepFace returns a list
    if isinstance(result, list):
        result = result[0]

    # extract summary fields
    emotion = result.get("dominant_emotion")
    age = result.get("age")
    gender = result.get("dominant_gender")

    # make sure age is JSON-serializable (convert numpy types)
    if isinstance(age, (np.generic,)):
        age = age.item()

    return {
        "emotion": emotion,
        "age": age,
        "gender": gender
    }

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    print("➡ /analyze hit")

    if "image" not in request.files:
        print("❌ no 'image' in request.files")
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    data = file.read()
    print(f"📦 got file, size = {len(data)} bytes")

    try:
        result = analyze_uploaded_image(data)
        print("✅ sending JSON response")
        return jsonify(result), 200
    except Exception as e:
        print("❌ ERROR in analyze:", repr(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask server running at http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)
