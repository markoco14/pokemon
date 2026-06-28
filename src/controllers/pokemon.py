import random
import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import queries
from src.dependencies import get_db
from src.types import Game, Pokemon
from src.utils import get_four_unique_numbers

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

from src.templates import templates

games = {}


async def index(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    
    pokemon = conn.execute(
        """
        SELECT w.word_id, w.word, w.thumbnail_img_path FROM word AS w 
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = 'pokemon';
        """
        ).fetchall()
        
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemon}
    )


async def whos_that(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    game_id = random.randint(1000, 10001)

    # TODO: change this back to only select 4 pokemon
    # requires some work because pokemon ids are lost
    # need some kind of word_meta table or pokemon_meta table 
    # to connect pokemon numbers to words
    pokemon = conn.execute(
        """
        SELECT w.word_id, w.word, w.large_img_path FROM word AS w 
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = 'pokemon';
        """
        ).fetchall()
    
    chosen_pokemon = random.sample(population=pokemon, k=4)
    
    answer = chosen_pokemon[random.randint(0,3)]

    games[game_id] = Game(
        id=game_id,
        answer=answer,
        pokemons=chosen_pokemon,
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

    if guess_pokemon_id == games[game_id].answer["word_id"]:
        games[game_id].finished = True
    
    return RedirectResponse(url=f"/whos-that-pokemon/{game_id}")
