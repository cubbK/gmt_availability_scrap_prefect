from typing import List
from typing_extensions import TypedDict


class Game(TypedDict):
    game_id: str
    game_name: str


games: List[Game] = [
    {
        "game_id": "18375",
        "game_name": "1846 Race for the Midwest",
    }
]
