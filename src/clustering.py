import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os

MODEL_PATH = "models/clustering_model.pkl"

FEATURES = [
    "annual_income",
    "spending_score",
    "purchase_frequency",
    "average_order_value",
    "last_purchase_days_ago"
]

# ---------------- TRAIN MODEL ----------------
def train_model(df):

    # Ensure models folder exists
    os.makedirs("models", exist_ok=True)

    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = model.fit_predict(X_scaled)

    # Save model safely
    try:
        joblib.dump((model, scaler), MODEL_PATH)
    except Exception as e:
        print("Model save failed:", e)

    return df


# ---------------- PREDICT ----------------
def predict_segment(input_df):

    # If model not available, return default cluster
    if not os.path.exists(MODEL_PATH):
        return [0]

    try:
        model, scaler = joblib.load(MODEL_PATH)

        X = input_df[FEATURES]
        X_scaled = scaler.transform(X)

        return model.predict(X_scaled)

    except Exception as e:
        print("Prediction error:", e)
        return [0]