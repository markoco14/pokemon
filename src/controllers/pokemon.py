import random

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import queries
from src.types import Game, Pokemon
from src.utils import get_four_unique_numbers

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

games = {}


async def index(request: Request):
    rows = queries.list_pokemon()

    pokemons = []
    for row in rows:
        pokemon = Pokemon(
            name=row[1],
            pokemon_id=row[2],
            pokemon_order=row[3],
            thumbnail=row[4]
        )
        pokemons.append(pokemon)
    
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemons}
    )


async def whos_that(request: Request):
    game_id = random.randint(1000, 10001)
    random_numbers = get_four_unique_numbers()
    rows = queries.get_whos_that_pokemon(random_numbers=random_numbers)

    pokemons = []
    for row in rows:
        pokemon = Pokemon(
                name=row[1],
                pokemon_id=row[2],
                pokemon_order=row[3],
                thumbnail=row[4]
            )
        pokemons.append(pokemon)

    answer = pokemons[random.randint(0,3)]

    games[game_id] = Game(
        id=game_id,
        answer=answer,
        pokemons=pokemons,
        guesses=[],
        finished=False
    )

    return RedirectResponse(url=f"/whos-that-pokemon/{game_id}")


async def pokemon_play(request: Request, game_id: int):
    if game_id not in games:
        return RedirectResponse(url="/", status_code=303)  

    return templates.TemplateResponse(
        request=request, name="whos-that-pokemon.html", context={"game": games[game_id]}
    )


def guess_that_pokemon(request: Request, game_id: int, guess_pokemon_id: int):
    if not games.get(game_id):
        return RedirectResponse(url="/", status_code=303)

    if guess_pokemon_id not in games[game_id].guesses:
        games[game_id].guesses.append(guess_pokemon_id)

    if guess_pokemon_id == games[game_id].answer.pokemon_id:
        games[game_id].finished = True
    
    return RedirectResponse(url=f"/whos-that-pokemon/{game_id}")
