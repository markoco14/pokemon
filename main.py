import sqlite3

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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

        pokemons = cursor.fetchall()
        
    except Exception as e:
        print(f"an error occured")

    finally:
        if connection:
            cursor.close()
            connection.close()
    
    return templates.TemplateResponse(
        request=request, name="pokemon/index.html", context={"pokemons": pokemons}
    )