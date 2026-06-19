import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'pharmacy.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    with open(os.path.join(os.path.dirname(__file__), '..', 'schema.sql'), 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
