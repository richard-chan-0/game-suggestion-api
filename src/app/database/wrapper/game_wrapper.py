from tinydb import TinyDB, Query
from dataclasses import asdict
from src.app.database.entities import *
from src.app.lib.exceptions import DataException
from src.app.database.entity_factory import (
    create_database_reader,
    create_database_query,
)
from src.app.database.constants import GAME_TABLE_NAME
import logging

logger = logging.getLogger(__name__)


games = create_database_reader(GAME_TABLE_NAME)
GameQuery = create_database_query()


def read_game(name: str):
    logger.info("searching for game with name: %s", name)
    existing_game = games.search(GameQuery.name == name)
    return existing_game[0] if existing_game else {}


def get_game_id(name: str):
    existing_game = read_game(name)
    return existing_game.doc_id if existing_game else -1


def get_game(game_id: int):
    game = games.get(doc_id=game_id)
    if not game:
        raise DataException("no game found")
    return game


def add_game(game: Game):
    logger.info("inserting new game: %s", game.name)
    existing_game = read_game(game.name)
    if existing_game:
        raise DataException(f"game already exists: {existing_game['name']}")
    return games.insert(asdict(game))


def remove_game(name: str):
    logger.info("removing game %s", name)
    games.remove(GameQuery.name == name)


def update_game(name: str, updates: dict):
    game_id = get_game_id(name)
    if game_id == -1:
        raise DataException("game does not exist")
    games.update(updates, doc_ids=[game_id])
