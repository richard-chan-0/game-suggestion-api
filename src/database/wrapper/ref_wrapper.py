from tinydb import TinyDB, Query
from dataclasses import asdict
from src.database.entities import *
from src.lib.exceptions import DataException
import logging

logger = logging.getLogger(__name__)

db = TinyDB("db.json")
refs = db.table("player_game_ref")

PlayerGameRefQuery = Query()


def add_player_game_ref(player_game_ref: PlayerGameRef):
    logger.info("inserting reference")
    refs.insert(asdict(player_game_ref))


def clean_player_games(steam_id: str):
    refs.remove(PlayerGameRefQuery.steam_id == steam_id)
