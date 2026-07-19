from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class DBGame:
    game_id: int
    url_path: str
    type: str
    category: str
    answer_id: int
    status: str
    created_at: datetime
    choice_ids: List[int]