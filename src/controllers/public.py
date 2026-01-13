from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import queries
from src.types import Pokemon

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

from src.templates import templates

games = {}


async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )
