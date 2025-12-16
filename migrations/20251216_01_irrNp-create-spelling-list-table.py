"""
Create spelling list table
"""

from yoyo import step

__depends__ = {'20251201_01_d6TZo-create-christmas-table'}

steps = [
    step("""CREATE TABLE spelling_list (
                list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
         """,
         "DROP TABLE spelling_list;")
]
