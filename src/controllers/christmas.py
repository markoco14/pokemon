import sqlite3
from typing import Annotated, TypedDict
from fastapi import FastAPI, Form, Request, Response

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.templates import templates

# class IndexPage(TypedDict):


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