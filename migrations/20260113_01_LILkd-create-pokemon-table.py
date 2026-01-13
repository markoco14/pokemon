"""
Create pokemon table
"""

from yoyo import step

__depends__ = {'20251216_02_jFdzj-create-spelling-list-word-table'}

steps = [
    step("""CREATE TABLE pokemon (
                pokemon_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                number INTEGER NOT NULL,
                img_path_thumbnail TEXT,
                img_path_large TEXT
         );""",
         "DROP TABLE IF EXISTS pokemon;")
]
