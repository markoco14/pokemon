-- Create word category table
-- depends: 20260628_02_uEZBh-create-category-table

CREATE TABLE IF NOT EXISTS word_category (
    word_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

INSERT INTO word_category (word_id, category_id)
SELECT word.word_id, category.category_id
FROM word
JOIN monster ON word.word = monster.name
JOIN category ON category.name = 'monster';

INSERT INTO word_category (word_id, category_id)
SELECT word.word_id, category.category_id
FROM word
JOIN christmas ON word.word = christmas.name
JOIN category ON category.name = 'christmas';

INSERT INTO word_category (word_id, category_id)
SELECT word.word_id, category.category_id
FROM word
JOIN pokemon ON word.word = pokemon.name
JOIN category ON category.name = 'pokemon';