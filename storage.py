# storage.py

import sqlite3
import os
from datetime import datetime

DB_PATH = "db/Trace.db"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            user TEXT,
            type TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_event(event):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO events (timestamp, ip, user, type)
        VALUES (?, ?, ?, ?)
    """, (event["timestamp"], event["ip"], event["user"], event["type"]))
    conn.commit()
    conn.close()
