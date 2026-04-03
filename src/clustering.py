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

def train_model(df):

    os.makedirs("models", exist_ok=True)

    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = model.fit_predict(X_scaled)

    # 🔥 SAFE SAVE
    try:
        joblib.dump((model, scaler), MODEL_PATH)
    except:
        pass

    return df