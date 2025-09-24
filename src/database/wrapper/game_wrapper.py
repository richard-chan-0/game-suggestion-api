from dataclasses import asdict
from src.database.entities import *
from src.lib.exceptions import DatabaseException
from src.database.entity_factory import (
    create_database_reader,
    create_database_query,
)
from src.database.constants import GAME_TABLE_NAME
import logging

logger = logging.getLogger(__name__)


def read_game(name: str):
    logger.info("searching for game with name: %s", name)
    db, games = create_database_reader(GAME_TABLE_NAME)
    game_query = create_database_query()
    try:
        existing_game = games.search(game_query.name == name)
        return existing_game[0] if existing_game else {}
    finally:
        db.close()


def get_game_id(name: str):
    existing_game = read_game(name)
    return existing_game.doc_id if existing_game else -1


def get_game(game_id: int):
    logger.info("finding game by id %s", game_id)
    db, games = create_database_reader(GAME_TABLE_NAME)
    try:
        game = games.get(doc_id=game_id)
        if not game:
            raise DatabaseException("no game found")
        return game
    finally:
        db.close()


def add_game(game: Game):
    logger.info("inserting new game: %s", game.name)
    existing_game = read_game(game.name)
    if existing_game:
        raise DatabaseException(f"game already exists: {existing_game['name']}")
    db, games = create_database_reader(GAME_TABLE_NAME)
    try:
        return games.insert(asdict(game))
    finally:
        db.close()


def remove_game(name: str):
    logger.info("removing game %s", name)
    db, games = create_database_reader(GAME_TABLE_NAME)
    games_query = create_database_query()
    try:
        games.remove(games_query.name == name)
    except Exception as e:
        raise DatabaseException(f"error removing game: {e}")
    finally:
        db.close()


def update_game(name: str, updates: dict):
    game_id = get_game_id(name)
    if game_id == -1:
        raise DatabaseException("game does not exist")
    db, games = create_database_reader(GAME_TABLE_NAME)
    try:
        games.update(updates, doc_ids=[game_id])
    except Exception as e:
        raise DatabaseException(f"error updating game: {e}")
    finally:
        db.close()


def get_all_games():
    db, games = create_database_reader(GAME_TABLE_NAME)
    try:
        return games.all()
    finally:
        db.close()
