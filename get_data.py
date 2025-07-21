import time
import requests
import json
import sqlite3

def get_all_pokemon_from_api():
    start_time = time.time()
    print("getting all pokemon")
    try:
        connection = sqlite3.connect('pokemon.db')

        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                pokemon_id INTEGER UNIQUE,
                pokemon_order INTEGER
            )
        ''')

        connection.commit()

        for i in range(1, 152):
            print(f"getting pokemon {i}")
            r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/")
            r.raise_for_status()


            name = r.json()["name"]
            pokemon_id = r.json()["id"]
            pokemon_order = r.json()["order"]

            cursor.execute("INSERT INTO pokemon (name, pokemon_id, pokemon_order) VALUES (?, ?, ?);", (name, pokemon_id, pokemon_order))
            print(f"pokemon stored: {name} - {pokemon_id} - {pokemon_order}")

        connection.commit()
        print(f"job took: {time.time() - start_time} seconds")
    
    except Exception as e:
        raise Exception(f"an error occured: {e}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()

def read_pokemon_from_db():
    try:
        connection = sqlite3.connect('pokemon.db')

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM pokemon;")

        rows = cursor.fetchall()

        for row in rows:
            print(row)

    except Exception as e:
        print(f"an error occured: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

def delete_all_in_db():
    try:
        connection = sqlite3.connect('pokemon.db')

        cursor = connection.cursor()

        cursor.execute("DELETE FROM pokemon WHERE id >= 1;")

        connection.commit()

    except Exception as e:
        print(f"an error occured: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

read_pokemon_from_db()
# delete_all_in_db()
# read_pokemon_from_db()

# get_all_pokemon_from_api()