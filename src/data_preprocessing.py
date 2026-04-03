import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path):
    return pd.read_csv(path)

def preprocess(df):
    df = df.copy()

    df['last_purchase_days_ago'] = df['last_purchase_days_ago'].clip(0, 365)

    return df

def scale_features(df, features):
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])
    return scaled, scaler
