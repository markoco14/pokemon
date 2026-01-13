import sqlite3
import time
from types import SimpleNamespace
import requests
import re

from bs4 import BeautifulSoup, SoupStrainer

from src.queries import list_pokemon
from src.types import Pokemon

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"


def new_scrape_thumbnails():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    gen1_heading = soup.find("span", id="Generation_I")
    if not gen1_heading:
        raise RuntimeError("Generation I heading not found")
    
    table = gen1_heading.find_parent("h3").find_next("table")
    if not table:
        raise RuntimeError("Table after Generation I not found")
    
    update_data = []
    rows = table.find_all("tr")
    for row in rows:

        # get td not th
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        id = cells[0].get_text(strip=True)
        if not id.startswith("#"):
            continue

        img = cells[1].find("img")
        if not img:
            continue

        img_src = img.get("src")

        stripped_id = id.lstrip("#").lstrip("0")
        update_data.append((img_src, stripped_id))

    with sqlite3.connect("esl.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.executemany("UPDATE pokemon SET img_path_thumbnail = ? WHERE pokemon_id = ?;", update_data)


def scrape_large_images(url="https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pokémon)"):
    base_url = "https://bulbapedia.bulbagarden.net/wiki/"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # get image
    table = soup.find("table", class_="roundy infobox")

    rows = table.find_all("tr")
    th = rows[0].find("th")
    id = th.find("span").get_text()
    stripped_id = int(id.lstrip("#").lstrip("0"))
    large_img = rows[0].find("img")
    img_src = large_img.get("src")

    if stripped_id > 151:
        return
    
    with sqlite3.connect("esl.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE pokemon SET img_path_large = ? WHERE pokemon_id = ?;", (img_src, stripped_id))

    next_link_target = f"#{stripped_id + 1:04d}"
    first_table = soup.find_all("table")[0]
    span = first_table.find("span", string=re.compile(next_link_target))

    a = span.find_parent("a")
    href = a.get("href")

    new_url = base_url + href.split("/wiki/")[1]

    time.sleep(0.5)

    scrape_large_images(new_url)




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
                    img_path_thumbnail=thumbnails_to_keep[row[0]-1]
                )

    # update rows in the database
    update_params = [(value.thumbnail, value.pokemon_id) for value in pokemon_dict.values()]
    try:
        with sqlite3.connect("esl.db") as connection:
            cursor = connection.cursor()

            cursor.executemany(
                '''UPDATE pokemon SET img_path_thumbnail = ? WHERE id = ?''',
                update_params
            )

            connection.commit()

    except Exception as e:
        raise Exception(f"an error occured: {e}")
