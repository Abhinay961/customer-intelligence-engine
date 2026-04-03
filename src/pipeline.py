from src.db import fetch_data, get_connection
from src.feature_engineering import create_features
from src.clustering import train_model
from src.utils import map_cluster_to_segment

def run_pipeline():

    # Load from DB
    df = fetch_data("SELECT * FROM customers")

    # Feature engineering
    df = create_features(df)

    # Train clustering
    df = train_model(df)

    # Map segments
    df = map_cluster_to_segment(df)

    # Save back to DB
    conn = get_connection()
    df.to_sql("segmented_customers", conn, if_exists="replace", index=False)
    conn.close()

    return df