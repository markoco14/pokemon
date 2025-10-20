from dataclasses import dataclass
import random
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
    def get(cls, monster_id):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monster WHERE monster_id=?;", (monster_id, ))
            row = cursor.fetchone()

            return Monster(
                monster_id=row["monster_id"],
                name=row["name"],
                large_img_path=row["large_img_path"],
                thumbnail_img_path=row["thumbnail_img_path"]
            )

    @classmethod
    def create(cls, name: str, large_img_path: str):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")

            cursor = conn.cursor()
            cursor.execute("INSERT INTO monster (name, large_img_path) VALUES (?, ?);", (name, large_img_path))
            return cursor.lastrowid
        
    @classmethod
    def get_random(cls):
        monsters = Monster.list()
        number_of_monsters = len(monsters)
        random_index = random.randint(1, number_of_monsters)

        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monster WHERE monster_id=?;", (random_index, ))
            row = cursor.fetchone()

            monster = Monster(
                monster_id=row["monster_id"],
                name=row["name"],
                large_img_path=row["large_img_path"],
                thumbnail_img_path=row["thumbnail_img_path"]
            )
                
            return monster
        
    @classmethod
    def get_by_name(cls, name: str):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monster WHERE name=?;", (name, ))
            row = cursor.fetchone()

            return Monster(
                monster_id=row["monster_id"],
                name=row["name"],
                large_img_path=row["large_img_path"],
                thumbnail_img_path=row["thumbnail_img_path"]
            )
        
    def update(self, name: str, large_img_path: str):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("UPDATE monster SET name=?, large_img_path=? WHERE monster_id=?;", (name, large_img_path, self.monster_id))
            
    def update_name(self, name: str):
        with sqlite3.connect("esl.db") as conn:
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor.execute("UPDATE monster SET name=? WHERE monster_id=?;", (name, self.monster_id))