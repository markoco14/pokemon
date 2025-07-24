import sqlite3
from typing import List


def list_pokemon():
    try:
        connection = sqlite3.connect('pokemon.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pokemon;")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        raise Exception(f"an error occured: {e}") from e
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_whos_that_pokemon(random_numbers: List[int]) -> List[any]:
    try:
        connection = sqlite3.connect("pokemon.db")
        cursor = connection.cursor()
        placeholders = ', '.join('?' * len(random_numbers))
        query = f"SELECT * FROM pokemon WHERE id IN ({placeholders});"
        cursor.execute(query, random_numbers)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"There was an error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()
