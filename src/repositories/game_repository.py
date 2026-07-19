import json
import sqlite3
from typing import List


def list_by_category(conn: sqlite3.Connection, category: str):
    return conn.execute(
        "SELECT * FROM game WHERE category = :category;", 
        {"category": category}
        ).fetchall()


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
