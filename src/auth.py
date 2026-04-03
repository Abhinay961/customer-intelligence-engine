import sqlite3
import hashlib

DB_PATH = "data/database.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)

    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    ).fetchone()

    conn.close()

    return user is not None