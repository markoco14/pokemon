from typing import Annotated, TypedDict
from fastapi import FastAPI, Form, Request, Response

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

class MonsterEditPage(TypedDict):
    monster: Monster
    name_error: str

async def monster_edit(request: Request, name: str):
    monster = Monster.get_by_name(name=name)

    return templates.TemplateResponse(
        request=request,
        name="halloween/monsters/edit.html",
        context=MonsterEditPage(
            monster=monster,
            name_error=""
        )
    )

async def monster_update(request: Request, name: str, monster_name: Annotated[str, Form()]):
    """Updates a monster resource."""
    monster = Monster.get_by_name(name=name)

    if not monster:
        return Response(status_code=200, headers={"hx-redirect": "/halloween"})

    if monster_name == "":
        name_error = "The monster needs to have a name"
        return templates.TemplateResponse(
            request=request,
            name="halloween/monsters/edit.html",
            context=MonsterEditPage(
                monster=monster,
                name_error=name_error
            )
        )
    
    monster.update_name(name=monster_name)

    return Response(status_code=200, headers={"hx-redirect": f"/halloween/monsters/{monster_name}/edit"})
    
