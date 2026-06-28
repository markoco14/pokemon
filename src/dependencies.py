import sqlite3
from typing import Generator


def get_db() -> Generator:
    conn = sqlite3.connect("esl.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()