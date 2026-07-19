import sqlite3
import requests
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH=os.environ.get("DB_PATH")
S3_FOLDER=os.environ.get("S3_FOLDER")

def update_pokemon_img_paths(conn, pokemon_name):
    """Downloads an image from a URL and uploads it directly to S3."""
    thumb_key = f"{S3_FOLDER}/{pokemon_name}_thumb.png"
    large_key = f"{S3_FOLDER}/{pokemon_name}_large.png"

    conn.execute(
        """
        UPDATE word 
        SET large_img_path = :large_img_path, thumbnail_img_path = :thumbnail_img_path 
        WHERE LOWER(word) = :pokemon_name;
        """, 
        {
            "large_img_path": large_key, 
            "thumbnail_img_path": thumb_key, 
            "pokemon_name": pokemon_name
        }
        )
    

def main():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT word, large_img_path, thumbnail_img_path 
    FROM word 
    JOIN word_category ON word.word_id = word_category.word_id
    WHERE word_category.category_id = 3;
    """

    try:
        rows = conn.execute(query).fetchall()

        for row in rows:
            pokemon_name, large_url, thumb_url = row
            pokemon_name = str(pokemon_name).strip().lower()
            update_pokemon_img_paths(conn=conn, pokemon_name=pokemon_name)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"something went wrong with get pokemon query: {e}")
    finally:
        conn.close()
        print("images uploaded")

    print("done")

if __name__ == "__main__":
    main()