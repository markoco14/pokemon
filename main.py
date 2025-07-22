import sqlite3
from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@dataclass
class Pokemon:
    name: str
    pokemon_id: int
    pokemon_order: int


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@app.get("/pokemon")
async def pokemon_index(request: Request):
    
    try:
        connection = sqlite3.connect('pokemon.db')

        cursor = connection.cursor()\
        
        cursor.execute("SELECT * FROM pokemon;")

        rows = cursor.fetchall()

        pokemons = []
        for row in rows:
            pokemon = Pokemon(
                name=row[1],
                pokemon_id=row[2],
                pokemon_order=row[3]
            )
            pokemons.append(pokemon)

    except Exception as e:
        print(f"an error occured")

    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemons}
    )

@app.get("/pokemon/play")
async def pokemon_play(request: Request):
    return templates.TemplateResponse(
        request=request, name="pokemon/play.html", context={}
    )