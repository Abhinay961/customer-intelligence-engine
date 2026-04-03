import sqlite3

conn = sqlite3.connect("data/database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

print("✅ Users table created")