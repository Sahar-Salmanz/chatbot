import sqlite3
from contextlib import contextmanager


DB_PATH = "app.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()

    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT,
                email    TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            ); 
            CREATE TABLE IF NOT EXISTS topic_stats (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                topic      TEXT NOT NULL,
                count      INTEGER DEFAULT 1,
                UNIQUE(user_email, topic)
            );
        """)

def upsert_topic(user_email: str, topic: str):
    """Insert topic if new, otherwise increment its count.
    """
    with get_db() as conn:
        conn.execute("""
            INSERT INTO topic_stats (user_email, topic, count)
            VALUES (?, ?, 1)
            ON CONFLICT(user_email, topic)
            DO UPDATE SET count = count + 1
        """, (user_email, topic))

def get_top_topics(user_email: str, limit: int=5) -> list[dict]:
    """Return the top N topics for a user, sorted by count desc.
    """
    with get_db() as conn:
        rows = conn.execute("""
            SELECT topic, count
            FROM topic_stats
            WHERE user_email = ?
            ORDER BY count DESC
            LIMIT ?
        """, (user_email, limit)).fetchall()
    return [{"topic": row["topic"], "count": row["count"]} for row in rows]