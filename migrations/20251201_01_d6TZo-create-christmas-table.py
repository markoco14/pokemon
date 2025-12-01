"""
Create christmas table
"""

from yoyo import step

__depends__ = {'20251020_01_1B4Kz-create-monster-table'}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS christmas (
            christmas_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            large_img_path TEXT,
            thumbnail_img_path TEXT,
            alt_text TEXT
        );
        """,
        "DROP TABLE IF EXISTS christmas;")
]
