from src.database.entities import *
from src.lib.string_utils import clean_name


def create_player(steam_id, first_name, last_name):
    return Player(steam_id, first_name, last_name)


def create_game(app_id, name):
    return Game(app_id, name)


def create_game_from_response(response):
    app_id = response["appid"]
    name = clean_name(response["name"])
    return create_game(app_id, name)


def create_reference(steam_id, app_id):
    return PlayerGameRef(steam_id, app_id)
