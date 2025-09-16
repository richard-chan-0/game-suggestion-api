from tinydb import TinyDB, Query
from dataclasses import asdict
from src.app.database.entities import *
from src.app.lib.exceptions import DataException
import logging

logger = logging.getLogger(__name__)

db = TinyDB("db.json")
players = db.table("players")

PlayerQuery = Query()


def read_player(steam_id: str):
    logger.info("finding player")
    players_found = players.search(PlayerQuery.steam_id == steam_id)
    return {} if not players_found else players_found[0]


def read_player_by_name(first_name: str, last_name: str):
    logger.info("finding player by name: %s %s", first_name, last_name)
    players_found = players.search(
        (PlayerQuery.first_name == first_name) & (PlayerQuery.last_name == last_name)
    )
    return {} if not players_found else players_found[0]


def get_player_by_id(id: int):
    logger.info("finding player by id %s", id)
    players_found = players.get(doc_id=id)
    return {} if not players_found else players_found


def get_player_id(steam_id):
    logger.info("finding player id %s", steam_id)
    existing_player = read_player(steam_id)
    return existing_player.doc_id if existing_player else -1


def add_player(player: Player):
    logger.info("inserting new player")
    existing_player = read_player(player.steam_id)
    if existing_player:
        raise DataException("player already onboarded")

    return players.insert(asdict(player))


def get_all_players():
    return [player for player in players.all()]


def remove_player(steam_id: str):
    players.remove(PlayerQuery.steam_id == steam_id)


def update_player(steam_id: str, updates: dict):
    id = get_player_id(steam_id)
    if id == -1:
        raise DataException("no player found")
    players.update(updates, doc_ids=[id])
