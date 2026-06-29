import random
import sqlite3
from typing import Annotated, TypedDict
from fastapi import Depends, FastAPI, Form, Request, Response

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from repositories import word_repository
from src.dependencies import get_db
from src.models.monster import Monster

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

from src.templates import templates


async def index(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    new_monsters = word_repository.list_by_category(conn=conn, category="monster")

    return templates.TemplateResponse(
        request=request,
        name="halloween/index.html",
        context={
            "monsters": new_monsters
        }
    )


async def monster_show(
        request: Request,
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    new_monster = word_repository.get(conn=conn, word_id=monster_id)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/show.html",
        context={
            "monster": new_monster
        }
    )


async def monster_edit(
        request: Request, 
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    new_monster = word_repository.get(conn=conn, word_id=monster_id)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/edit.html",
        context={
            "monster": new_monster,
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
    new_monster_name = name

    new_monster = word_repository.get(conn=conn, word_id=monster_id)

    if not new_monster:
        return Response(status_code=200, headers={"hx-redirect": "/halloween"})

    if new_monster_name == "":
        name_error = "The monster needs to have a name"
        return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/edit.html",
            context={
                "monster": new_monster,
                "name_error": name_error
            }
        )

    try:
        word_repository.update(
            conn=conn, 
            new_word=new_monster_name, 
            new_large_img_path=large_img, 
            word_id=monster_id)
        conn.commit()
    except Exception:
        return Response(status_code=500, content="something went wrong")
    
    return Response(
        status_code=200, 
        headers={"hx-redirect": f"/halloween/monsters/{new_monster['word_id']}/edit"}
        )
    

async def monster_teach(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    new_monsters = word_repository.list_by_category(conn=conn, category="monster")

    return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/teach.html",
            context={
                "monsters": new_monsters
            }
        )

async def monster_see_and_say(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    new_monsters = word_repository.list_by_category(conn=conn, category="monster")
    number_of_monsters = len(new_monsters)
    
    if not request.query_params.get("monster"):
        random_index = random.randint(1, number_of_monsters)        
        monster = word_repository.get(conn=conn, word_id=random_index)
        
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={monster['word']}")

    new_monster = word_repository.get_by_word(conn=conn, word=request.query_params.get("monster"))

    if not new_monster:
        random_index = random.randint(1, number_of_monsters)
        new_monster = word_repository.get(conn=conn, word_id=random_index)
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={new_monster['word']}")

    random_index = random.randint(1, number_of_monsters)
    next_monster = word_repository.get(conn=conn, word_id=random_index)
    
    while next_monster["word"] == new_monster["word"]:
        random_index = random.randint(1, number_of_monsters)
        next_monster = word_repository.get(conn=conn, word_id=random_index)

    return templates.TemplateResponse(
        request=request,
        name=f"halloween/monsters/see-and-say.html",
        context={
            "monster": new_monster,
            "next_monster": next_monster
        }
    )