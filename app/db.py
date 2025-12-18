# app/db.py
import sqlite3

DB_PATH = "memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_conversation(user_msg, bot_msg):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (user_message, bot_response)
        VALUES (?, ?)
    ''', (user_msg, bot_msg))
    conn.commit()
    conn.close()