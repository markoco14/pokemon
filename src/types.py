from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pokemon:
    name: str
    pokemon_id: int
    pokemon_order: int
    thumbnail: Optional[str] = ''

@dataclass
class Game:
    id: int
    answer: Pokemon
    pokemons: List[Pokemon]
    guesses: List[int]
    finished: bool