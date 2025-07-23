import sqlite3


def list_pokemon():
    try:
        connection = sqlite3.connect('pokemon.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pokemon;")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"an error occured")
    finally:
        if connection:
            cursor.close()
            connection.close()
