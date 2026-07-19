-- Create game tables
-- depends: 20260628_03_4XSnT-create-word-category-table


CREATE TABLE game(
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_path TEXT UNIQUE NOT NULL,
    type TEXT CHECK (type IN ('mc')) NOT NULL,
    category TEXT NOT NULL,
    answer_id INTEGER NOT NULL,
    status TEXT CHECK (status IN ('active', 'won', 'lost')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(answer_id) REFERENCES word(word_id)
);

CREATE TABLE game_guess(
    guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    is_correct INTEGER CHECK (is_correct IN (0, 1)) NOT NULL,
    guessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(game_id) REFERENCES game(game_id),
    FOREIGN KEY(word_id) REFERENCES word(word_id)
);