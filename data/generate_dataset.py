import pandas as pd
import numpy as np
import random

np.random.seed(42)

n = 60000

customer_id = np.arange(1, n+1)

age = np.random.randint(18, 65, n)

gender = np.random.choice(['Male', 'Female'], n)

annual_income = np.random.normal(60000, 20000, n).clip(20000, 150000)

purchase_frequency = np.random.poisson(10, n)

average_order_value = (annual_income / 20) * np.random.uniform(0.5, 1.5, n)

spending_score = (purchase_frequency * average_order_value) / 1000

last_purchase_days_ago = np.random.exponential(scale=30, size=n)

preferred_category = np.random.choice(
    ['Electronics', 'Fashion', 'Grocery', 'Sports', 'Home'], n
)

df = pd.DataFrame({
    "customer_id": customer_id,
    "age": age,
    "gender": gender,
    "annual_income": annual_income,
    "spending_score": spending_score,
    "purchase_frequency": purchase_frequency,
    "average_order_value": average_order_value,
    "last_purchase_days_ago": last_purchase_days_ago,
    "preferred_category": preferred_category
})

df.to_csv("data/customers.csv", index=False)
