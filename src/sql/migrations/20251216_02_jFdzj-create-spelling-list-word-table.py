"""
Create spelling list word table
"""

from yoyo import step

__depends__ = {'20251216_01_irrNp-create-spelling-list-table'}

steps = [
    step("""CREATE TABLE spelling_list_word (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                list_id INTEGER NOT NULL,
                FOREIGN KEY(list_id) REFERENCES spelling_list(list_id)
            );
         """,
         "DROP TABLE spelling_list_word;")
]
