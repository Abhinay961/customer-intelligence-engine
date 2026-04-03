import pandas as pd

def create_features(df):
    df = df.copy()

    # CLV
    df['clv'] = df['purchase_frequency'] * df['average_order_value'] * 12

    # 🔥 SAFE RFM (NO qcut crash)
    df['recency_score'] = pd.cut(df['last_purchase_days_ago'], bins=4, labels=[4,3,2,1])
    df['frequency_score'] = pd.cut(df['purchase_frequency'], bins=4, labels=[1,2,3,4])
    df['monetary_score'] = pd.cut(df['average_order_value'], bins=4, labels=[1,2,3,4])

    df['rfm_score'] = (
        df['recency_score'].astype(int) +
        df['frequency_score'].astype(int) +
        df['monetary_score'].astype(int)
    )

    return df