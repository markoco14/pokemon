from dataclasses import dataclass
from typing import Optional


@dataclass
class Word:
    word_id: int
    word: str
    large_img_path: Optional[str]
    thumbnail_img_path: Optional[str]