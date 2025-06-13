from dataclasses import dataclass


@dataclass
class Player:
    steam_id: str
    first_name: str
    last_name: str


@dataclass
class Game:
    app_id: str
    name: str


@dataclass
class PlayerGameRef:
    player_id: str
    game_id: str
