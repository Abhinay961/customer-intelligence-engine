import pandas as pd
import sqlite3

df = pd.read_csv("data/customers.csv")

conn = sqlite3.connect("data/database.db")

# Raw table
df.to_sql("customers", conn, if_exists="replace", index=False)

print("✅ Raw data loaded")

conn.close()