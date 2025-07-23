import random
import sqlite3
from dataclasses import dataclass
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

games = {}
@dataclass
class Pokemon:
    name: str
    pokemon_id: int
    pokemon_order: int

@dataclass
class Game:
    id: int
    answer: Pokemon
    pokemons: List[Pokemon]
    guesses: List[int]
    finished: bool

def get_four_unique_numbers() -> List[int]:
    unique = False
    random_numbers = []
    while unique == False:
        random_number = random.randint(1, 151)
        if random_number not in random_numbers:
            random_numbers.append(random_number)
        if len(random_numbers) == 4:
            unique = True

    return random_numbers

def get_four_pokemon(random_numbers: List[int]) -> List[Pokemon]:
    pokemons = []
    try:
        connection = sqlite3.connect("pokemon.db")
        cursor = connection.cursor()
        for number in random_numbers:
            cursor.execute(f"SELECT * FROM pokemon WHERE id = {number}")
            row = cursor.fetchone()
            pokemon = Pokemon(
                name=row[1],
                pokemon_id=row[2],
                pokemon_order=row[3]
            )
            pokemons.append(pokemon)
    except Exception as e:
        print(f"There was an error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

    return pokemons


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )


@app.get("/pokemon")
async def pokemon_index(request: Request):
    try:
        connection = sqlite3.connect('pokemon.db')

        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM pokemon;")

        rows = cursor.fetchall()

        pokemons = []
        for row in rows:
            pokemon = Pokemon(
                name=row[1],
                pokemon_id=row[2],
                pokemon_order=row[3]
            )
            pokemons.append(pokemon)

    except Exception as e:
        print(f"an error occured")

    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemons}
    )


@app.get("/pokemon/play")
async def pokemon_play(request: Request):
    game_id = random.randint(1000, 10001)
    random_numbers = get_four_unique_numbers()
    pokemons = get_four_pokemon(random_numbers=random_numbers)
    answer = pokemons[random.randint(0,3)]

    games[game_id] = Game(
        id=game_id,
        answer=answer,
        pokemons=pokemons,
        guesses=[],
        finished=False
    )

    return RedirectResponse(url=f"/pokemon/play/{game_id}")


@app.get("/pokemon/play/{game_id}")
async def pokemon_play(request: Request, game_id: int):
    if game_id not in games:
        return RedirectResponse(url="/pokemon", status_code=303)  

    return templates.TemplateResponse(
        request=request, name="pokemon/play.html", context={"game": games[game_id]}
    )


@app.get("/pokemon/play/{game_id}/{guess_pokemon_id}")
def guess_that_pokemon(request: Request, game_id: int, guess_pokemon_id: int):
    if not games.get(game_id):
        return RedirectResponse(url="/pokemon", status_code=303)

    if guess_pokemon_id not in games[game_id].guesses:
        games[game_id].guesses.append(guess_pokemon_id)

    if guess_pokemon_id == games[game_id].answer.pokemon_id:
        games[game_id].finished = True
    
    return RedirectResponse(url=f"/pokemon/play/{game_id}")
