import sqlite3
import time

import requests

from src.types import Pokemon


def get_first_generation_from_api():
    print("checking if pokemon already in db")
    
    start_time = time.time()
    print("getting all pokemon")
    pokemon_data_for_bulk_insert = []
    
    try:
        with sqlite3.connect("pokemon.db") as connection:
            cursor = connection.cursor()

            # check if pokemon already in DB
            cursor.execute("SELECT COUNT(*) FROM pokemon;")
            existing_pokemon_count = cursor.fetchone()[0]
            if existing_pokemon_count >= 1: # Assuming we only ever insert 151
                print(f"Database already contains {existing_pokemon_count} Pokemon. Skipping API fetch and population.")
                return # Exit early if already populated

            for i in range(1, 152):
                print(f"getting pokemon {i}")
                r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/")
                r.raise_for_status()

                name = r.json()["name"]
                pokemon_id = r.json()["id"]
                pokemon_order = r.json()["order"]

                pokemon_data_for_bulk_insert.append((name, pokemon_id, pokemon_order))
                print(f"got pokemon from api: {name} - {pokemon_id} - {pokemon_order}")

            if not pokemon_data_for_bulk_insert:
                print("no pokemon.. bail out")
                return
           
            cursor.executemany(
                "INSERT OR IGNORE INTO pokemon (name, pokemon_id, pokemon_order) VALUES (?, ?, ?);",
                pokemon_data_for_bulk_insert
            )
            connection.commit()
            print(f"job took: {time.time() - start_time} seconds")    
    except Exception as e:
        raise Exception(f"an error occured: {e}") from e
