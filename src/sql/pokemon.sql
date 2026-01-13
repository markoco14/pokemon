CREATE TABLE pokemon (
                pokemon_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                number INTEGER NOT NULL,
                img_path_thumbnail TEXT,
                img_path_large TEXT
         );
