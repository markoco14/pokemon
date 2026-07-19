import json
import sqlite3
from typing import List


def list_by_category(conn: sqlite3.Connection, category: str):
    return conn.execute(
        "SELECT * FROM game WHERE category = :category;", 
        {"category": category}
        ).fetchall()

def get_by_url_path(conn: sqlite3.Connection, url_path: str):
        return conn.execute("SELECT * FROM game WHERE url_path = :url_path;", {"url_path": url_path}).fetchone()

def insert(
        conn: sqlite3.Connection, 
        url_path: str, 
        type: str, 
        category: str, 
        answer_id: int, 
        choice_ids: List[int]
        ):
    serialized_choice_ids = json.dumps(choice_ids)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO game (
        url_path, type, category, answer_id, choice_ids
        ) VALUES (
        :url_path, :type, :category, :answer_id, :choice_ids
        );""", 
        {"url_path": url_path, 
         "type": type, 
         "category": category, 
         "answer_id": answer_id, 
         "choice_ids": serialized_choice_ids
         })
    conn.commit()


def set_game_won(conn: sqlite3.Connection, url_path: str):
    conn.execute("UPDATE game SET status = 'won' WHERE url_path = :url_path", {"url_path": url_path})