import random
import sqlite3
from typing import Annotated
from fastapi import Depends, Request

from fastapi.responses import RedirectResponse

from src.dependencies import get_db
from src.templates import templates

async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="christmas/index.html",
        context={}
    )


async def teach(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    
    rows = conn.execute(
        """
        SELECT w.word_id, w.word, w.large_img_path FROM word AS w
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = 'christmas';
        """
        ).fetchall()
    
    return templates.TemplateResponse(
        request=request,
        name="christmas/teach.html",
        context={"vocab_set": rows}
    )


def get_random_word(conn: sqlite3.Connection):

    rows = conn.execute(
        """
        SELECT w.word_id, w.word, w.large_img_path FROM word AS w
        JOIN word_category AS wc ON wc.word_id = w.word_id
        JOIN category AS c ON c.category_id = wc.category_id
        WHERE c.name = 'christmas';
        """
        ).fetchall()

    random_index = random.randrange(len(rows))

    return rows[random_index]


async def see_and_say(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    if not request.query_params.get("word"):
        word = get_random_word(conn=conn)
        return RedirectResponse(status_code=303, url=f"/christmas/see-and-say?word={word['word']}")
    
    word = conn.execute(
        "SELECT * FROM word WHERE word = :word;", 
        {"word": request.query_params.get("word")}
        ).fetchone()

    next_word = get_random_word(conn=conn)
    while next_word["word"] == word["word"]:
        next_word = get_random_word(conn=conn)
    
    return templates.TemplateResponse(
        request=request,
        name=f"christmas/see-and-say.html",
        context={
            "word": word,
            "next_word": next_word
        }
    )
