import pickle
import os

def load_model():
    model_path = os.path.join("model", "edu2job_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model
