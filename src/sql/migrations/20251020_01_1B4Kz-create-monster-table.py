"""
Create monster table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS monster (
            monster_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            large_img_path TEXT,
            thumbnail_img_path TEXT
        );
        """,
        "DROP TABLE IF EXISTS monster;")
]
