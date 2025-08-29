import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# Path setup
DATA_PATH = os.path.join("..", "dataset", "edu2job_dataset.csv")
MODEL_PATH = os.path.join("model", "edu2job_model.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)

# Combine text features
df["text"] = (
    df["degree"].astype(str) + " " +
    df["major"].astype(str) + " " +
    df["cgpa"].astype(str) + " " +
    df["skills"].astype(str)
)

X = df["text"]
y = df["job_role"]

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# Save model + vectorizer
os.makedirs("model", exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model trained and saved at", MODEL_PATH)
