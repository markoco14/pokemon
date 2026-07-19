CREATE TABLE game(
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_path TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('mc')) NOT NULL,
    category TEXT NOT NULL,
    answer_id INTEGER NOT NULL,
    status TEXT CHECK (status IN ('active', 'won', 'lost')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    choice_ids TEXT,
    FOREIGN KEY(answer_id) REFERENCES word(word_id)
);
