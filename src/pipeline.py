import os
import pandas as pd
import numpy as np

from src.db import get_connection
from src.feature_engineering import create_features
from src.clustering import train_model
from src.utils import map_cluster_to_segment

DATA_PATH = "data/customers.csv"

def generate_data():
    n = 50000

    df = pd.DataFrame({
        "customer_id": range(n),
        "age": np.random.randint(18, 65, n),
        "annual_income": np.random.randint(20000, 150000, n),
        "spending_score": np.random.randint(1, 100, n),
        "purchase_frequency": np.random.randint(1, 30, n),
        "average_order_value": np.random.randint(100, 5000, n),
        "last_purchase_days_ago": np.random.randint(1, 180, n)
    })

    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

def run_pipeline():

    try:
        # 🔥 Ensure folders exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("models", exist_ok=True)

        # 🔥 Step 1: Dataset
        if not os.path.exists(DATA_PATH):
            generate_data()

        df = pd.read_csv(DATA_PATH)

        # 🔥 Step 2: Features
        df = create_features(df)

        # 🔥 Step 3: Clustering
        df = train_model(df)

        # 🔥 Step 4: Segments
        df = map_cluster_to_segment(df)

        # 🔥 Step 5: Save DB
        conn = get_connection()
        df.to_sql("segmented_customers", conn, if_exists="replace", index=False)
        conn.close()

        return df

    except Exception as e:
        print("PIPELINE ERROR:", e)
    raise e