-- Create category table 
-- depends: 20260628_01_TJLBT-create-word-table

CREATE TABLE IF NOT EXISTS category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

INSERT INTO category (name) VALUES ('monster');
INSERT INTO category (name) VALUES ('christmas');
INSERT INTO category (name) VALUES ('pokemon');