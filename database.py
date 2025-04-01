# database.py
import sqlite3

DB_NAME = 'events.db'

def get_connection():
    """Establish and return a new SQLite connection."""
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create the events table if it doesn't already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,        -- Stored as 'YYYY-MM-DD'
                time_start TEXT NOT NULL,  -- Stored as 'HH:MM'
                time_end TEXT,             -- Optional
                type TEXT,
                location TEXT
            )
        ''')
        conn.commit()