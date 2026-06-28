import random
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
    large_img: Annotated[str, Form()],
    conn: Annotated[sqlite3.Connection, Depends(get_db)]
    ):
    """Updates a monster resource."""
    # monster = Monster.get(monster_id=monster_id)
    new_monster_name = name
    print(new_monster_name)

    new_monster = conn.execute(
        """
        SELECT word_id, word, large_img_path FROM word
        WHERE word_id = :word_id;
        """,
        {"word_id": monster_id}
    ).fetchone()

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

    conn.execute(
        """
        UPDATE word 
        SET word = :word, large_img_path = :large_img_path
        WHERE word_id = :word_id;
        """,
        {
            "word": new_monster_name,
            "large_img_path": large_img,
            "word_id": monster_id
        }
    )
    conn.commit()

    return Response(status_code=200, headers={"hx-redirect": f"/halloween/monsters/{new_monster['word_id']}/edit"})
    

async def monster_teach(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
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
            name="halloween/monsters/teach.html",
            context={
                "monsters": new_monsters
            }
        )

async def monster_see_and_say(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    new_monsters = conn.execute(
            """
            SELECT w.word_id, w.word, w.large_img_path FROM word AS w 
            JOIN word_category AS wc ON wc.word_id = w.word_id
            JOIN category AS c ON c.category_id = wc.category_id
            WHERE c.name = 'monster';
            """
        ).fetchall()
    number_of_monsters = len(new_monsters)
    
    if not request.query_params.get("monster"):
        random_index = random.randint(1, number_of_monsters)
        monster = conn.execute("SELECT * FROM word WHERE word_id = :word_id;", {"word_id": random_index}).fetchone()
        return RedirectResponse(status_code=303, url=f"/halloween/monsters/see-and-say?monster={monster['word']}")

    new_monster = conn.execute(
        """
        SELECT word_id, word, large_img_path FROM word
        WHERE word = :word;
        """,
        {"word": request.query_params.get("monster")}
    ).fetchone()
    
    random_index = random.randint(1, number_of_monsters)
    next_monster = conn.execute("SELECT * FROM word WHERE word_id = :word_id;", {"word_id": random_index}).fetchone()
    
    while next_monster["word"] == new_monster["word"]:
        random_index = random.randint(1, number_of_monsters)
        next_monster = conn.execute("SELECT * FROM word WHERE word_id = :word_id;", {"word_id": random_index}).fetchone()
    
    return templates.TemplateResponse(
        request=request,
        name=f"halloween/monsters/see-and-say.html",
        context={
            "monster": new_monster,
            "next_monster": next_monster
        }
    )