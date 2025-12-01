import random
import sqlite3
from fastapi import Request

from fastapi.responses import RedirectResponse

from src.templates import templates

async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="christmas/index.html",
        context={}
    )


async def teach(request: Request):
    with sqlite3.connect("esl.db") as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM christmas;")
        vocab_set = cursor.fetchall()

    
    return templates.TemplateResponse(
        request=request,
        name="christmas/teach.html",
        context={"vocab_set": vocab_set}
    )


def get_random_word():
    with sqlite3.connect("esl.db") as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM christmas;")
        vocab_set = cursor.fetchall()

    random_index = random.randrange(len(vocab_set))

    return vocab_set[random_index]


async def see_and_say(request: Request):
    if not request.query_params.get("word"):
        word = get_random_word()
        return RedirectResponse(status_code=303, url=f"/christmas/see-and-say?word={word['name']}")
    
    with sqlite3.connect("esl.db") as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM christmas WHERE name = ?;", (request.query_params.get("word"),))
        word = cursor.fetchone()

    next_word = get_random_word()
    while next_word["name"] == word["name"]:
        next_word = get_random_word()
    
    return templates.TemplateResponse(
        request=request,
        name=f"christmas/see-and-say.html",
        context={
            "word": word,
            "next_word": next_word
        }
    )
