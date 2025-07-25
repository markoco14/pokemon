import time
import requests
import json
import sqlite3

DATABASE_FILE = "pokemon.db"

# 001 create pokemon table

def create_pokemon_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE pokemon (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    pokemon_id INTEGER UNIQUE,
                    pokemon_order INTEGER
                )
            ''')
            connection.commit()
            print("pokemon table created successfully.")
    except Exception as e:
        raise Exception(f"an erorr occured: {e}") from e
        

def drop_pokemon_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS  pokemon;''')
            connection.commit()
    except Exception as e:
        raise Exception(f"an erorr occured: {e}") from e
    
# 002 add thumbnail to pokemon table

def add_thumbnail_to_pokemon_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("PRAGMA table_info(pokemon);")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            if "thumbnail" in column_names:
                print("warning column exists.. bail out")
                return
            else:
                print('no such column')

            cursor.execute('''ALTER TABLE pokemon ADD COLUMN thumbnail TEXT DEFAULT '';''')

            connection.commit()
            print("thumnail column added successfully")

    except Exception as e:
        raise Exception(f"an error occured: {e}") from e
    

def drop_thumbnail_from_pokemon_table():
    try:
        with sqlite3.connect(DATABASE_FILE) as connection:
            cursor = connection.cursor()

            cursor.execute("PRAGMA table_info(pokemon);")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            if "thumbnail" not in column_names:
                print("warning no thumbnail column exists.. bail out")
                return

            cursor.execute('''ALTER TABLE pokemon DROP COLUMN thumbnail;''')
            connection.commit()
            print("thumnail column dropped from pokemon table.")
    except Exception as e:
        raise Exception(f"an error occured: {e}") from e
