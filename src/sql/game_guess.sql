CREATE TABLE game_guess(
    guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    is_correct INTEGER CHECK (is_correct IN (0, 1)) NOT NULL,
    guessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(game_id) REFERENCES game(game_id),
    FOREIGN KEY(word_id) REFERENCES word(word_id)
);
