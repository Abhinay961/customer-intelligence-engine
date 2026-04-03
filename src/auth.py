import sqlite3
import hashlib
import os

DB_PATH = "data/database.db"

def get_connection():
    # 🔥 Ensure folder exists
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users_table():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_user(username, password):
    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()

    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hash_password(password))
        ).fetchone()
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

    return user is not None