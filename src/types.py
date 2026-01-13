from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pokemon:
    pokemon_id: int
    name: str
    number: int
    img_path_thumbnail: Optional[str] = ""
    img_path_large: Optional[str] = ""

@dataclass
class Game:
    id: int
    answer: Pokemon
    pokemons: List[Pokemon]
    guesses: List[int]
    finished: bool