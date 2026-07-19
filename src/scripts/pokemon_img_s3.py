import sqlite3
import requests
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client("s3")

DB_PATH=os.environ.get("DB_PATH")
S3_BUCKET=os.environ.get("S3_BUCKET")
S3_FOLDER=os.environ.get("S3_FOLDER")

if not DB_PATH:
    raise ValueError("DB path missing. Please check .env file.")

def download_and_upload_to_s3(pokemon_name, url, is_thumbnail=False):
    """Downloads an image from a URL and uploads it directly to S3."""
    if not url or url.isspace():
        return
    
    url = url.strip()

    ext = 'jpg' if '.jpg' in url.lower() or '.jpeg' in url.lower() else 'png'

    suffix = 'thumb' if is_thumbnail else 'large'

    s3_key = f"{S3_FOLDER}/{pokemon_name}_{suffix}.{ext}"

    try:
        if is_thumbnail:
            print(f"getting {pokemon_name} thumbnail")
        else:
            print(f"getting {pokemon_name} large")
            
        response = requests.get(url)
        response.raise_for_status()

        if is_thumbnail:
            print(f"uploading {pokemon_name} thumbnail")
        else:
            print(f"uploading {pokemon_name} large")

        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=response.content,
            ContentType=response.headers.get("Content-Type", "image/{ext}")
        )
    except Exception as e:
        if is_thumbnail:
            print(f"error uploading {pokemon_name} thumbnail: {e}")
        else:
            print(f"error uploading {pokemon_name} large: {e}")



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

    except Exception as e:
        print("something went wrong with get pokemon query")
    finally:
        conn.close()
        print("images uploaded")

    try:
        for row in rows:
            pokemon_name, large_img, thumb_img = row
            pokemon_name = str(pokemon_name).strip().lower()
            download_and_upload_to_s3(pokemon_name, large_img, is_thumbnail=False)
            download_and_upload_to_s3(pokemon_name, thumb_img, is_thumbnail=True)
    except Exception as e:
        print("something went wrong uploading images")

    print("done")

if __name__ == "__main__":
    main()