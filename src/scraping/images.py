# step 1 just get the images
# save them to a text file with pokemon id - name - image url (or json)
# then you can check that out and see if anything is missing or wrong
# then you can use that to write to the db
# I need to update the DB, so I'll have to figure out some kind of migrations system
# or use SQL Alchemy
# Might be fun to use ALCHEMY with raw SQL or Postgres

from pprint import pprint
import requests

from bs4 import BeautifulSoup, SoupStrainer

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

# def WIP_scrape_links_to_detail_pages():
#     r = requests.get(URL)
#     text = r.text
#     only_tables = SoupStrainer('table')

#     soup = BeautifulSoup(text, "html.parser", parse_only=only_tables)
#     first_table = soup.find('table', class_='roundy')

#     needed_links = first_table.select('a[title*=Pokémon]')

#     pprint(needed_links)
#     print(f"job complete")

