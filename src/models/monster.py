from dataclasses import dataclass
import sqlite3


@dataclass
class Monster:
    monster_id: int
    name: str
    large_img_path: str
    thumbnail_img_path: str

    @classmethod
    def list(cls):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monster;")
            rows = cursor.fetchall()

            monsters: list[Monster] = []
            for row in rows:
                monster = Monster(
                    monster_id=row["monster_id"],
                    name=row["name"],
                    large_img_path=row["large_img_path"],
                    thumbnail_img_path=row["thumbnail_img_path"]
                )
                monsters.append(monster)

            return monsters

    @classmethod
    def create(cls, name: str):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")

            cursor = conn.cursor()
            cursor.execute("INSERT INTO monster (name) VALUES (?);", (name, ))
            return cursor.lastrowid