from typing import TypedDict
from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.models.monster import Monster

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

class IndexPage(TypedDict):
    monsters: list[Monster]

async def index(request: Request):

    monsters = Monster.list()
    return templates.TemplateResponse(
        request=request,
        name="halloween/index.html",
        context=IndexPage(
            monsters=monsters
        )
    )


class MonsterShowPage(TypedDict):
    monster: Monster

async def monster_show(request: Request, name: str):
    monster = Monster.get_by_name(name=name)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/show.html",
        context=MonsterShowPage(
            monster=monster
        )
    )