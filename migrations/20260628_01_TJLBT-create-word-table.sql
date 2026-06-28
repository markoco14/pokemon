-- Create word table 
-- depends: 20260113_01_LILkd-create-pokemon-table

CREATE TABLE IF NOT EXISTS word (
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    large_img_path TEXT,
    thumbnail_img_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

INSERT INTO word (word, large_img_path, thumbnail_img_path)
SELECT name, large_img_path, thumbnail_img_path
FROM monster;

INSERT INTO word (word, large_img_path, thumbnail_img_path)
SELECT name, large_img_path, thumbnail_img_path
FROM christmas;

INSERT INTO word (word, large_img_path, thumbnail_img_path)
SELECT name, img_path_large, img_path_thumbnail
FROM pokemon;