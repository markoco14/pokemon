from fastapi import APIRouter, Depends

from src.controllers import pokemon, public


router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'dependencies')
routes = [
    ("GET", "/", public.root),   # None
    ("GET", "/whos-that-pokemon", pokemon.whos_that),
    ("GET", "/whos-that-pokemon/{game_id}", pokemon.pokemon_play), 
    ("GET", "/whos-that-pokemon/{game_id}/{guess_pokemon_id}", pokemon.guess_that_pokemon), 
]

for method, path, handler in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
    )


