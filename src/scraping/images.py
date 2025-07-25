import sqlite3
import requests
import re

from bs4 import BeautifulSoup, SoupStrainer

from src.queries import list_pokemon
from src.types import Pokemon

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"


def scrape_pokemon_thumbnails():
    r = requests.get(URL)
    text = r.text
    only_tables = SoupStrainer('table')
    soup = BeautifulSoup(text, "html.parser", parse_only=only_tables)
    first_table = soup.find('table', class_='roundy')
    images = first_table.find_all('img')
    with open("./images.txt", "a") as text_file:
        for image in images:
            text_file.write(image.attrs["src"])
            text_file.write("\n")
 
    print(f"job complete")


def store_thumbnails_links():
    print(f"Running script to store thumbnail links")
    pokemon_rows = list_pokemon()
    reg_filter = r"-[A-Za-z_]+"
    pokemon_dict = {}

    # filter out images of pokemon alternatives
    thumbnails_to_keep = []
    with open("./images.txt", "r") as thumbnail_file:
        thumbnail_links = thumbnail_file.read().splitlines()
        for link in thumbnail_links:
            if re.search(reg_filter, link):
                print(f'found one to remove: {link}')
                # del thumbnail_links[index]
            else:
                print(f'found one to keep: {link}')
                thumbnails_to_keep.append(link)

    # match pokemon rows with thumbnails
    # create Pokemon objects for each to make it easier to work with
    for row in pokemon_rows:
        if row[0] < 10:
            number_to_find = f"000{row[0]}"
            if number_to_find in thumbnails_to_keep[row[0]-1]:
                pokemon_dict[f"000{row[0]}"] = Pokemon(
                    name=row[1],
                    pokemon_id=row[2],
                    pokemon_order=row[3],
                    thumbnail=thumbnails_to_keep[row[0]-1]
                )
        elif row[0] >= 10 and row[0] < 100:
            number_to_find = f"00{row[0]}"
            if number_to_find in thumbnails_to_keep[row[0]-1]:
                pokemon_dict[f"00{row[0]}"] = Pokemon(
                    name=row[1],
                    pokemon_id=row[2],
                    pokemon_order=row[3],
                    thumbnail=thumbnails_to_keep[row[0]-1]
                )
        else:
            number_to_find = f"0{row[0]}"
            if number_to_find in thumbnails_to_keep[row[0]-1]:
                pokemon_dict[f"0{row[0]}"] = Pokemon(
                    name=row[1],
                    pokemon_id=row[2],
                    pokemon_order=row[3],
                    thumbnail=thumbnails_to_keep[row[0]-1]
                )

    # update rows in the database
    update_params = [(value.thumbnail, value.pokemon_id) for value in pokemon_dict.values()]
    try:
        with sqlite3.connect("pokemon.db") as connection:
            cursor = connection.cursor()

            cursor.executemany(
                '''UPDATE pokemon SET thumbnail = ? WHERE id = ?''',
                update_params
            )

            connection.commit()

    except Exception as e:
        raise Exception(f"an error occured: {e}")
