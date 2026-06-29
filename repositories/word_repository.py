import sqlite3


def list_by_category(conn: sqlite3.Connection, category: str):
    return conn.execute(
        """
        SELECT w.word_id, w.word, w.large_img_path FROM word AS w 
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = :category;
        """,
        {"category": category}
    ).fetchall()


def get(conn: sqlite3.Connection, word_id: int):
    return conn.execute(
        """
        SELECT word_id, word, large_img_path FROM word
        WHERE word_id = :word_id;
        """,
        {"word_id": word_id}
    ).fetchone()


def get_by_word(conn: sqlite3.Connection, word: str):
    return conn.execute(
        """
        SELECT word_id, word, large_img_path FROM word
        WHERE word = :word;
        """,
        {"word": word}
    ).fetchone()
    

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