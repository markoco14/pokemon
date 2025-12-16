CREATE TABLE spelling_list_word (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                list_id INTEGER NOT NULL,
                FOREIGN KEY(list_id) REFERENCES spelling_list(list_id)
            );