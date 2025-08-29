from flask import Blueprint, request, jsonify
import os, pickle

pred_bp = Blueprint('pred_bp', __name__)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "edu2job_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

try:
    with open(MODEL_PATH, "rb") as f:
        vectorizer, model = pickle.load(f)
    print("✅ Model loaded:", MODEL_PATH)
except Exception as e:
    vectorizer, model = None, None
    print("❌ Model load failed:", e)

@pred_bp.route('', methods=['POST'])
def predict():
    if vectorizer is None or model is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.json
    text = " ".join([
        data.get("degree",""),
        data.get("major",""),
        str(data.get("cgpa","")),
        data.get("skills","")
    ])
    X_vec = vectorizer.transform([text])
    prediction = model.predict(X_vec)[0]

    return jsonify({"prediction": prediction})
