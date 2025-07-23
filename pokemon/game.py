import random
import sqlite3

from src.main import Pokemon

def choose_pokemon():
    random_number = random.randint(1, 151)
    print(f"choosing pokemon for {random_number}")
    try:
        connection = sqlite3.connect("pokemon.db")

        cursor = connection.cursor()
        
        cursor.execute(f"SELECT * FROM pokemon WHERE id = {random_number}")

        row = cursor.fetchone()

        print(row)

    except Exception as e:
        print(f"something went wrong getting the pokemon: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()

    pokemon = Pokemon(
        name=row[1],
        pokemon_id=row[2],
        pokemon_order=row[3]
    )
    
    return pokemon

def play():
    pokemon = choose_pokemon()
    print(f"pokemon chosen for the game: {pokemon}")
    print("game over")

play()