import random
import sqlite3
from typing import List


def list_by_category(conn: sqlite3.Connection, category: str) -> List[sqlite3.Row]:
    return conn.execute(
        """
        SELECT w.word_id, w.word, w.large_img_path, w.thumbnail_img_path FROM word AS w 
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = :category;
        """,
        {"category": category}
    ).fetchall()


def get_count_by_category(conn: sqlite3.Connection, category: str) -> int:
    return conn.execute(
        """
        SELECT COUNT(*) 
        FROM word AS w 
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = :category;
        """,
        {"category": category}
    ).fetchone()[0]


def get(conn: sqlite3.Connection, word_id: int) -> sqlite3.Row:
    return conn.execute(
        """
        SELECT word_id, word, large_img_path, thumbnail_img_path FROM word
        WHERE word_id = :word_id;
        """,
        {"word_id": word_id}
    ).fetchone()


def get_game_choices(conn: sqlite3.Connection, choice_ids):
    return conn.execute(
        "SELECT * FROM word WHERE word_id IN (SELECT value FROM json_each(:choice_ids));", 
        {"choice_ids": choice_ids}
        ).fetchall()


def get_by_word(conn: sqlite3.Connection, word: str) -> sqlite3.Row:
    return conn.execute(
        """
        SELECT word_id, word, large_img_path, thumbnail_img_path FROM word
        WHERE word = :word;
        """,
        {"word": word}
    ).fetchone()


def get_random_word_by_category(conn: sqlite3.Connection, category: str):
    words = list_by_category(conn=conn, category=category)
    choice = random.choice(words)

    return choice
    

def update(conn: sqlite3.Connection, new_word: str, new_large_img_path: str, word_id: int):
    conn.execute(
        """
        UPDATE word 
        SET word = :word, large_img_path = :large_img_path
        WHERE word_id = :word_id;
        """,
        {
            "word": new_word,
            "large_img_path": new_large_img_path,
            "word_id": word_id
        }
    )