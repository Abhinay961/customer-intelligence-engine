import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

MODEL_PATH = "models/clustering_model.pkl"

FEATURES = [
    "annual_income",
    "spending_score",
    "purchase_frequency",
    "average_order_value",
    "last_purchase_days_ago"
]

def train_model(df):

    X = df[FEATURES]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=4, random_state=42)
    df['cluster'] = model.fit_predict(X_scaled)

    joblib.dump((model, scaler), MODEL_PATH)

    return df


def load_model():
    return joblib.load(MODEL_PATH)


def predict_segment(input_df):

    model, scaler = load_model()
    X = scaler.transform(input_df[FEATURES])

    return model.predict(X)