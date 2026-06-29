import random
import sqlite3
from typing import Annotated
from fastapi import Depends, Request

from fastapi.responses import RedirectResponse

from repositories import word_repository
from src.dependencies import get_db
from src.templates import templates

async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="christmas/index.html",
        context={}
    )


async def teach(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    words = word_repository.list_by_category(conn=conn, category="christmas")
    
    return templates.TemplateResponse(
        request=request,
        name="christmas/teach.html",
        context={"vocab_set": words}
    )


async def see_and_say(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    query_word = request.query_params.get("word")
    if not query_word:
        word = word_repository.get_random_word_by_category(conn=conn, category="christmas")
        return RedirectResponse(status_code=303, url=f"/christmas/see-and-say?word={word['word']}")
    
    word = word_repository.get_by_word(conn=conn, word=query_word)

    next_word = word_repository.get_random_word_by_category(conn=conn, category="christmas")
    while next_word["word"] == word["word"]:
        next_word = word_repository.get_random_word_by_category(conn=conn, category="christmas")
    
    return templates.TemplateResponse(
        request=request,
        name=f"christmas/see-and-say.html",
        context={
            "word": word,
            "next_word": next_word
        }
    )
