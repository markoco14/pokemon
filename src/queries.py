import sqlite3
from typing import List


def list_pokemon():
    try:
        with sqlite3.connect("esl.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pokemon;")
            rows = cursor.fetchall()
    except Exception as e:
        print(f"an error occurred geting pokemon: {e}")
    
    return rows

   

def get_whos_that_pokemon(random_numbers: List[int]) -> List[any]:
    try:
        with sqlite3.connect("esl.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            placeholders = ', '.join('?' * len(random_numbers))
            query = f"SELECT * FROM pokemon WHERE pokemon_id IN ({placeholders});"
            cursor.execute(query, random_numbers)
            rows = cursor.fetchall()
    except Exception as e:
        print(f"an error occurred getting whos that pokemon: {e}")

    return rows
