from tinydb import TinyDB, Query
from dataclasses import asdict
from src.database.entities import *
from src.lib.exceptions import DataException
import logging

logger = logging.getLogger(__name__)

db = TinyDB("db.json")
games = db.table("games")

GameQuery = Query()


def add_game(game: Game):
    logger.info("inserting new game: %s", game.name)
    games.insert(asdict(game))
