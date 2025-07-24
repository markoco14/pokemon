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



# def read_pokemon_from_db():
#     try:
#         connection = sqlite3.connect('pokemon.db')

#         cursor = connection.cursor()

#         cursor.execute("SELECT * FROM pokemon;")

#         rows = cursor.fetchall()

#         for row in rows:
#             print(row)

#     except Exception as e:
#         print(f"an error occured: {e}")

#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# def delete_all_in_db():
#     try:
#         connection = sqlite3.connect('pokemon.db')

#         cursor = connection.cursor()

#         cursor.execute("DELETE FROM pokemon WHERE id >= 1;")

#         connection.commit()

#     except Exception as e:
#         print(f"an error occured: {e}")

#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# read_pokemon_from_db()
# delete_all_in_db()
# read_pokemon_from_db()

# get_all_pokemon_from_api()