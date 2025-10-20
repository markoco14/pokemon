from fastapi import APIRouter, Depends

from src.controllers import halloween, pokemon, public


router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'dependencies')
routes = [
    ("GET", "/", public.root),

    ("GET", "/pokemon", pokemon.index),
    ("GET", "/whos-that-pokemon", pokemon.whos_that),
    ("GET", "/whos-that-pokemon/{game_id}", pokemon.pokemon_play),
    ("GET", "/whos-that-pokemon/{game_id}/{guess_pokemon_id}", pokemon.guess_that_pokemon),

    ("GET", "/halloween", halloween.index),
    ("GET", "/halloween/monsters/{monster_id}", halloween.monster_show),
    ("GET", "/halloween/monsters/{name}/edit", halloween.monster_edit),
    ("PUT", "/halloween/monsters/{name}", halloween.monster_update),

]

for method, path, handler in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
    )


