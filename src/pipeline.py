import os
import pandas as pd

from src.db import get_connection
from src.feature_engineering import create_features
from src.clustering import train_model
from src.utils import map_cluster_to_segment

DATA_PATH = "data/customers.csv"

def generate_data():
    import numpy as np

    n = 60000

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

    # 🔥 Step 1: Ensure dataset exists
    if not os.path.exists(DATA_PATH):
        print("Generating dataset...")
        generate_data()

    # 🔥 Step 2: Load dataset
    df = pd.read_csv(DATA_PATH)

    # 🔥 Step 3: Feature engineering
    df = create_features(df)

    # 🔥 Step 4: Clustering
    df = train_model(df)

    # 🔥 Step 5: Segment mapping
    df = map_cluster_to_segment(df)

    # 🔥 Step 6: Save to DB
    conn = get_connection()
    df.to_sql("segmented_customers", conn, if_exists="replace", index=False)
    conn.close()

    return df