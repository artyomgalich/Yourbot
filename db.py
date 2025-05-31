import sqlite3
from datetime import datetime

DB_NAME = "jur_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Користувачі
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        registered_at TEXT,
        paid INTEGER DEFAULT 0
    )
    """)

    # Історія заяв
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zayavy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, name=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (user_id, name, registered_at) VALUES (?, ?, ?)",
                   (user_id, name, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def set_paid(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET paid=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_paid(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT paid FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] == 1 if row else False

def add_zayava(user_id, type_):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO zayavy (user_id, type, created_at) VALUES (?, ?, ?)",
                   (user_id, type_, datetime.now().isoformat()))
    conn.commit()
    conn.close()
