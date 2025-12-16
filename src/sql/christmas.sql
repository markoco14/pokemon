CREATE TABLE christmas (
            christmas_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            large_img_path TEXT,
            thumbnail_img_path TEXT,
            alt_text TEXT
        );