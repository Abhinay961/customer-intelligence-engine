import pandas as pd

def create_features(df):
    df = df.copy()

    df['clv'] = df['purchase_frequency'] * df['average_order_value'] * 12

    df['recency_score'] = pd.qcut(df['last_purchase_days_ago'], 4, labels=[4,3,2,1])
    df['frequency_score'] = pd.qcut(df['purchase_frequency'], 4, labels=[1,2,3,4])
    df['monetary_score'] = pd.qcut(df['average_order_value'], 4, labels=[1,2,3,4])

    df['rfm_score'] = (
        df['recency_score'].astype(int) +
        df['frequency_score'].astype(int) +
        df['monetary_score'].astype(int)
    )

    return df