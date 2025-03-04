from typing import List
from typing_extensions import TypedDict


class Game(TypedDict):
    game_id: str
    game_name: str


games: List[Game] = [
    {
        "game_id": "18375",
        "game_name": "1846 Race for the Midwest",
    },
    {
        "game_id": "30541",
        "game_name": "1848: Australia",
    },
    {
        "game_id": "41240",
        "game_name": "18 India",
    },
    {
        "game_id": "544",
        "game_name": "1960: The Making of the President",
    },
    {"game_id": "35020", "game_name": "Men of Iron Tri-Pack"},
    {"game_id": "34371", "game_name": "Congress of Vienna"},
    {"game_id": "9539", "game_name": "Unconditional Surrender! World War 2 in Europe"},
    {
        "game_id": "40710",
        "game_name": "Prime Minister",
    },
]
