CREATE TABLE monster (
            monster_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            large_img_path TEXT,
            thumbnail_img_path TEXT
        );