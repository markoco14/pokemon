import sqlite3


def list_by_category(conn: sqlite3.Connection, category: str):
    return conn.execute(
        "SELECT * FROM game WHERE category = :category;", 
        {"category": category}
        ).fetchall()


def insert(conn: sqlite3.Connection, url_path: str, type: str, category: str, answer_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO game (url_path, type, category, answer_id) VALUES (:url_path, :type, :category, :answer_id)", 
        {"url_path": url_path, "type": type, "category": category, "answer_id": answer_id})
