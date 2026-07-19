import secrets
import random
import sqlite3
from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi.responses import RedirectResponse

from src.repositories import game_repository, word_repository
from src.dependencies import get_db
from src.templates import templates
from src.utils import get_s3_domain


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


async def whos_that_pokemon_game(
        request: Request, 
        conn: Annotated[sqlite3.Connection, Depends(get_db)],
        url_path: str):
    
    try:
        game_row = game_repository.get_by_url_path(conn=conn, url_path=url_path)
    except Exception as e:
        return Response(status_code=500, content="something went wrong")

    if not game_row:
        return Response(status_code=404, content="Game not found")

    try:
        choice_rows = word_repository.get_game_choices(conn=conn, choice_ids=game_row["choice_ids"])
    except Exception as e:
        return Response(status_code=500, content="something went wrong")
    
    choices_dict = {row["word_id"]: dict(row) for row in choice_rows}
    s3_domain = get_s3_domain()
    for key, value in choices_dict.items():
        value["large_img_path"] = f'{s3_domain}/{value["large_img_path"]}'
    
    answer = choices_dict.get(game_row["answer_id"])

    return templates.TemplateResponse(
        request=request,
        name="pokemon/v2-whos-that-pokemon.html",
        context={
            "game": game_row,
            "choices": choices_dict,
            "answer": answer
        }
    )


def whos_that_pokemon_guess(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)],
        url_path: str, 
        guess_id: int
        ):
    
    try:
        game_row = game_repository.get_by_url_path(conn=conn, url_path=url_path)
    except Exception as e:
        return Response(status_code=500, content="something went wrong")
    
    try:
        word_row = word_repository.get(conn=conn, word_id=guess_id)
    except Exception as e:
        return Response(status_code=500, content="something went wrong")

    word = dict(word_row)
    s3_domain = get_s3_domain()
    word["large_img_path"] = f'{s3_domain}/{word["large_img_path"]}'

    if guess_id == game_row["answer_id"]:
        return templates.TemplateResponse(
            request=request,
            name="pokemon/game-option-oob.html",
            context={
                "style": "correct",
                "game": game_row,
                "choice": word,
                "is_correct": True
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="pokemon/game-option-oob.html",
        context={
            "style": "wrong",
            "game": game_row,
            "choice": word,
        }
    )
