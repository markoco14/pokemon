import random
import sqlite3
from typing import Annotated
from fastapi import Depends, FastAPI, Form, Request, Response

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from repositories import word_repository
from src.dependencies import get_db

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

from src.templates import templates


async def index(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    monsters = word_repository.list_by_category(conn=conn, category="monster")

    return templates.TemplateResponse(
        request=request,
        name="halloween/index.html",
        context={
            "monsters": monsters
        }
    )


async def monster_show(
        request: Request,
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    monster = word_repository.get(conn=conn, word_id=monster_id)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/show.html",
        context={
            "monster": monster
        }
    )


async def monster_edit(
        request: Request, 
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    monster = word_repository.get(conn=conn, word_id=monster_id)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/edit.html",
        context={
            "monster": monster,
            "name_error": ""
        }
    )

async def monster_update(
    request: Request,
    monster_id: str,
    name: Annotated[str, Form()],
    large_img: Annotated[str, Form()],
    conn: Annotated[sqlite3.Connection, Depends(get_db)]
    ):
    """Updates a monster resource."""
    form_name = name
    form_img = large_img

    monster = word_repository.get(conn=conn, word_id=monster_id)

    if not monster:
        return Response(status_code=200, headers={"hx-redirect": "/halloween"})

    if form_name == "":
        name_error = "The monster needs to have a name"
        return HTMLResponse(
            content=f'<p id="name_error" class="error">{name_error}</p>',
            headers={"Hx-Retarget": "#name_error"}
            )
    
    if form_img == "":
        image_error = "The monster needs to have an image url"
        return HTMLResponse(
            content=f'<p id="image_error" class="error">{image_error}</p>',
            headers={"Hx-Retarget": "#image_error"}
            )

    try:
        word_repository.update(
            conn=conn, 
            new_word=form_name, 
            new_large_img_path=large_img, 
            word_id=monster_id)
        conn.commit()
    except Exception:
        return Response(status_code=500, content="something went wrong")
    
    return Response(
        status_code=200, 
        headers={"hx-redirect": f"/halloween/monsters/{monster['word_id']}/edit"}
        )
    

async def monster_teach(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    monsters = word_repository.list_by_category(conn=conn, category="monster")

    return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/teach.html",
            context={
                "monsters": monsters
            }
        )

async def monster_see_and_say(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    number_of_monsters = word_repository.get_count_by_category(conn=conn, category="monster")
    request_monster_name = request.query_params.get("monster")
    
    if not request_monster_name:
        random_index = random.randint(1, number_of_monsters)        
        monster = word_repository.get(conn=conn, word_id=random_index)
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={monster['word']}")

    this_monster = word_repository.get_by_word(conn=conn, word=request_monster_name)
    if not this_monster:
        random_index = random.randint(1, number_of_monsters)
        monster = word_repository.get(conn=conn, word_id=random_index)
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={monster['word']}")

    random_index = random.randint(1, number_of_monsters)
    next_monster = word_repository.get(conn=conn, word_id=random_index)
    while next_monster["word"] == this_monster["word"]:
        random_index = random.randint(1, number_of_monsters)
        next_monster = word_repository.get(conn=conn, word_id=random_index)

    return templates.TemplateResponse(
        request=request,
        name=f"halloween/monsters/see-and-say.html",
        context={
            "monster": this_monster,
            "next_monster": next_monster
        }
    )