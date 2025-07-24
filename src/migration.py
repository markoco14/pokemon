import time
import requests
import json
import sqlite3

def create_pokemon_table():
    try:
        with sqlite3.connect('pokemon.db') as connection:
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
        with sqlite3.connect('pokemon.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS  pokemon;''')
            connection.commit()
    except Exception as e:
        raise Exception(f"an erorr occured: {e}") from e
