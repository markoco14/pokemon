from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import queries
from src.types import Pokemon

app = FastAPI()

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

games = {}


async def root(request: Request):
    rows = queries.list_pokemon()

    pokemons = []
    for row in rows:
        pokemon = Pokemon(
            name=row[1],
            pokemon_id=row[2],
            pokemon_order=row[3],
            thumbnail=row[4]
        )
        pokemons.append(pokemon)
    
    return templates.TemplateResponse(
        request=request, name="index.html", context={"pokemons": pokemons}
    )
