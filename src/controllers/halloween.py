import sqlite3
from typing import Annotated, TypedDict
from fastapi import Depends, FastAPI, Form, Request, Response

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.dependencies import get_db
from src.models.monster import Monster

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

from src.templates import templates

class IndexPage(TypedDict):
    monsters: list[Monster]

async def index(
        request: Request,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):

    new_monsters = conn.execute(
        """
            SELECT w.word_id, w.word, w.large_img_path FROM word AS w 
            JOIN word_category AS wc ON wc.word_id = w.word_id
            JOIN category AS c ON c.category_id = wc.category_id
            WHERE c.name = 'monster';
        """
    ).fetchall()
    
    return templates.TemplateResponse(
        request=request,
        name="halloween/index.html",
        context=IndexPage(
            monsters=new_monsters
        )
    )


class MonsterShowPage(TypedDict):
    monster: Monster

async def monster_show(
        request: Request,
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):
    
    new_monster = conn.execute(
        """
            SELECT word_id, word, large_img_path FROM word
            WHERE word_id = :word_id;
        """,
        {"word_id": monster_id}
    ).fetchone()

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/show.html",
        context=MonsterShowPage(
            monster=new_monster
        )
    )


async def monster_edit(
        request: Request, 
        monster_id: str,
        conn: Annotated[sqlite3.Connection, Depends(get_db)]
        ):

    new_monster = conn.execute(
        """
            SELECT word_id, word, large_img_path FROM word
            WHERE word_id = :word_id;
        """,
        {"word_id": monster_id}
    ).fetchone()

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
    large_img: Annotated[str, Form()]
    ):
    """Updates a monster resource."""
    monster = Monster.get(monster_id=monster_id)
    new_monster_name = name

    if not monster:
        return Response(status_code=200, headers={"hx-redirect": "/halloween"})

    if new_monster_name == "":
        name_error = "The monster needs to have a name"
        return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/edit.html",
            context=MonsterEditPage(
                monster=monster,
                name_error=name_error
            )
        )
    
    monster.update(name=new_monster_name, large_img_path=large_img)

    return Response(status_code=200, headers={"hx-redirect": f"/halloween/monsters/{monster.monster_id}/edit"})
    
class MonsterTeachPage(TypedDict):
    monsters: list[Monster]

async def monster_teach(request: Request):
    monsters = Monster.list()
    
    return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/teach.html",
            context=MonsterTeachPage(
                monsters=monsters
            )
        )

async def monster_see_and_say(request: Request):
    if not request.query_params.get("monster"):
        monster = Monster.get_random()
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={monster.name}")
    
    monster = Monster.get_by_name(name=request.query_params.get("monster"))

    next_monster = Monster.get_random()
    while next_monster.name == monster.name:
        next_monster = Monster.get_random()
    
    return templates.TemplateResponse(
        request=request,
        name=f"halloween/monsters/see-and-say.html",
        context={
            "monster": monster,
            "next_monster": next_monster
        }
    )