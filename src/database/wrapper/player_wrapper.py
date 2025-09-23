from dataclasses import asdict
from src.database.entities import *
from src.lib.exceptions import DatabaseException
from src.database.constants import PLAYER_TABLE_NAME
from src.database.entity_factory import (
    create_database_reader,
    create_database_query,
)
import logging

logger = logging.getLogger(__name__)


def read_player(steam_id: str):
    logger.info("finding player")
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    player_query = create_database_query()
    try:
        players_found = players.search(player_query.steam_id == steam_id)
        return {} if not players_found else players_found[0]
    finally:
        db.close()


def read_player_by_name(first_name: str, last_name: str):
    logger.info("finding player by name: %s %s", first_name, last_name)
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    player_query = create_database_query()
    query = (player_query.first_name == first_name) & (
        player_query.last_name == last_name
    )
    try:
        players_found = players.search(query)
        return {} if not players_found else players_found[0]
    finally:
        db.close()


def get_player_by_id(id: int):
    logger.info("finding player by id %s", id)
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    try:
        players_found = players.get(doc_id=id)
        return {} if not players_found else players_found
    finally:
        db.close()


def get_player_id(steam_id):
    logger.info("finding player id %s", steam_id)
    existing_player = read_player(steam_id)
    return existing_player.doc_id if existing_player else -1


def add_player(player: Player):
    logger.info("inserting new player")
    existing_player = read_player(player.steam_id)
    if existing_player:
        raise DatabaseException("player already onboarded")

    db, players = create_database_reader(PLAYER_TABLE_NAME)
    try:
        return players.insert(asdict(player))
    finally:
        db.close()


def get_all_players():
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    all_players = players.all()
    try:
        return [player for player in all_players]
    finally:
        db.close()


def remove_player(steam_id: str):
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    player_query = create_database_query()
    try:
        players.remove(player_query.steam_id == steam_id)
    finally:
        db.close()


def update_player(steam_id: str, updates: dict):
    id = get_player_id(steam_id)
    if id == -1:
        raise DatabaseException("no player found")
    db, players = create_database_reader(PLAYER_TABLE_NAME)
    try:
        players.update(updates, doc_ids=[id])
    finally:
        db.close()
