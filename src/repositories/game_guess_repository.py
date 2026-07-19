import sqlite3


def insert_correct_guess(conn: sqlite3.Connection, game_id: int, word_id: int):
    conn.execute(
                "INSERT INTO game_guess (game_id, word_id, is_correct) VALUES (:game_id, :word-id, :is_correct)", 
                {"game_id": game_id, "word_id": word_id, "is_correct": True}
                )


def insert_wrong_guess(conn: sqlite3.Connection, game_id: int, word_id: int):
    conn.execute(
                "INSERT INTO game_guess (game_id, word_id, is_correct) VALUES (:game_id, :word-id, :is_correct)", 
                {"game_id": game_id, "word_id": word_id, "is_correct": False}
                )