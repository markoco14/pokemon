import secrets
import os
import random
import sqlite3
from typing import Annotated
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.repositories import game_repository, word_repository
from src.dependencies import get_db
from src.types import Game

load_dotenv()


from src.templates import templates

games = {}


def get_s3_domain():
    aws_bucket = os.environ.get("S3_BUCKET")
    aws_region = os.environ.get("AWS_DEFAULT_REGION")
    return f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com"

async def index(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    pokemon_rows = word_repository.list_by_category(conn=conn, category="pokemon")
    s3_domain = get_s3_domain()
    pokemon_list = []
    for row in pokemon_rows:
        pokemon = dict(row)
        if pokemon["thumbnail_img_path"]:
            pokemon["thumbnail_img_path"] = f'{s3_domain}/{pokemon["thumbnail_img_path"]}'
        if pokemon["large_img_path"]:
            pokemon["large_img_path"] = f'{s3_domain}/{pokemon["large_img_path"]}'
        pokemon_list.append(pokemon)

        
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemon_list}
    )


async def whos_that_pokemon_redirect(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    game_id = random.randint(1000, 10001)

    # TODO: change this back to only select 4 pokemon
    # requires some work because pokemon ids are lost
    # need some kind of word_meta table or pokemon_meta table 
    # to connect pokemon numbers to words
    pokemon = word_repository.list_by_category(conn=conn, category="pokemon")
    
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


async def whos_that_pokemon_game(request: Request, game_id: int):
    if game_id not in games:
        return RedirectResponse(url="/", status_code=303)  

    return templates.TemplateResponse(
        request=request, name="pokemon/whos-that-pokemon.html", context={"game": games[game_id]}
    )

def whos_that_pokemon_guess(request: Request, game_id: int, guess_pokemon_id: int):
    if not games.get(game_id):
        return RedirectResponse(url="/", status_code=303)

    if guess_pokemon_id not in games[game_id].guesses:
        games[game_id].guesses.append(guess_pokemon_id)

    if guess_pokemon_id == games[game_id].answer["word_id"]:
        games[game_id].finished = True
    
    return RedirectResponse(url=f"/whos-that-pokemon/{game_id}")


async def whos_that_pokemon_redirect_v2(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    # TODO: change this back to only select 4 pokemon
    # requires some work because pokemon ids are lost
    # need some kind of word_meta table or pokemon_meta table 
    # to connect pokemon numbers to words
    pokemon = word_repository.list_by_category(conn=conn, category="pokemon")
    
    choices = random.sample(population=pokemon, k=4)
    choice_ids = [pokemon["word_id"] for pokemon in choices]
    
    answer = choices[random.randint(0,3)]
    answer_id = answer["word_id"]

    url_path = secrets.token_urlsafe(12)

    game_repository.insert(
        conn=conn, 
        url_path=url_path, 
        type='mc', 
        category='whos-that-pokemon', 
        answer_id=answer_id,
        choice_ids=choice_ids)
 
    return RedirectResponse(url=f"/whos-that-pokemon/{url_path}")



async def whos_that_pokemon_game_v2(
        request: Request, 
        conn: Annotated[sqlite3.Connection, Depends(get_db)],
        url_path: str):
    
    game_row = conn.execute("SELECT * FROM game WHERE url_path = :url_path;", {"url_path": url_path}).fetchone()

    if not game_row:
        return Response(status_code=404, content="Game not found")

    choice_rows = conn.execute(
        "SELECT * FROM word WHERE word_id IN (SELECT value FROM json_each(:ids));", 
        {"ids": game_row["choice_ids"]}
        ).fetchall()
    
    choices = {row["word_id"]: dict(row) for row in choice_rows}
    s3_domain = get_s3_domain()
    for key, value in choices.items():
        value["large_img_path"] = f'{s3_domain}/{value["large_img_path"]}'
    
    answer = choices.get(game_row["answer_id"])

    return templates.TemplateResponse(
        request=request,
        name="pokemon/v2-whos-that-pokemon.html",
        context={
            "game": game_row,
            "choices": choices,
            "answer": answer
        }
    )


def whos_that_pokemon_guess_v2(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)],
        url_path: str, 
        guess_id: int
        ):
    
    game_row = conn.execute("SELECT * FROM game WHERE url_path = :url_path;", {"url_path": url_path}).fetchone()

    word_row = conn.execute("SELECT * FROM word WHERE word_id = :word_id;", {"word_id": guess_id}).fetchone()
    word = dict(word_row)
    s3_domain = get_s3_domain()
    word["large_img_path"] = f'{s3_domain}/{word["large_img_path"]}'

    if guess_id == game_row["answer_id"]:
        return templates.TemplateResponse(
            request=request,
            name="pokemon/game-option.html",
            context={
                "style": "correct",
                "game": game_row,
                "choice": word,
                "is_response": True,
                "is_correct": True
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="pokemon/game-option.html",
        context={
            "style": "wrong",
            "game": game_row,
            "choice": word,
            "is_response": True
        }
    )
