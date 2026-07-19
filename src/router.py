from fastapi import APIRouter, Depends

from src.controllers import halloween, pokemon, public, christmas, spelling


router = APIRouter()

# routes follow ('method', 'path', 'endpoint/handler', 'dependencies')
routes = [
    ("GET",     "/",                                                public.root),

    ("GET",     "/pokemon",                                         pokemon.index),
    # ("GET",     "/whos-that-pokemon",                               pokemon.whos_that_pokemon_redirect),
    # ("GET",     "/whos-that-pokemon/{game_id}",                     pokemon.whos_that_pokemon_game),
    # ("GET",     "/whos-that-pokemon/{game_id}/{guess_pokemon_id}",  pokemon.whos_that_pokemon_guess),
    ("GET",     "/whos-that-pokemon",                               pokemon.whos_that_pokemon_redirect_v2),
    ("GET",     "/whos-that-pokemon/{url_path}",                    pokemon.whos_that_pokemon_game_v2),
    ("GET",     "/whos-that-pokemon/{url_path}/{guess_id}",         pokemon.whos_that_pokemon_guess_v2),

    ("GET",     "/halloween",                                       halloween.index),
    ("GET",     "/halloween/monsters/teach",                        halloween.monster_teach),
    ("GET",     "/halloween/monsters/see-and-say",                  halloween.monster_see_and_say),
    ("GET",     "/halloween/monsters/{monster_id}",                 halloween.monster_show),
    ("GET",     "/halloween/monsters/{monster_id}/edit",            halloween.monster_edit),
    ("PUT",     "/halloween/monsters/{monster_id}",                 halloween.monster_update),

    ("GET",     "/christmas",                                       christmas.index),
    ("GET",     "/christmas/teach",                                 christmas.teach),
    ("GET",     "/christmas/see-and-say",                           christmas.see_and_say),

    ("GET",     "/spelling",                                        spelling.index),
    ("GET",     "/spelling/missing-letters/{list_id}",              spelling.missing_letters),

    ("GET",     "/spelling/lists/new",                              spelling.lists_new),
    ("POST",    "/spelling/lists",                                  spelling.lists_create),
]

for method, path, handler in routes:
    router.add_api_route(
        path=path,
        endpoint=handler,
        methods=[method],
    )


