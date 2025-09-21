from dataclasses import asdict
from src.app.database.entities import *
from src.app.lib.exceptions import DatabaseException
from src.app.database.constants import PLAYER_GAME_REF_TABLE_NAME
from src.app.database.entity_factory import (
    create_database_query,
    create_database_reader,
)
import logging

logger = logging.getLogger(__name__)


def get_refs_for_players(player_ids: list[int]):
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    player_game_ref_query = create_database_query()
    try:
        return refs.search(player_game_ref_query.player_id.one_of(player_ids))
    finally:
        db.close()


def get_refs_for_player(player_id: int):
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    player_game_ref_query = create_database_query()
    try:
        return refs.search(player_game_ref_query.player_id == player_id)
    finally:
        db.close()


def get_ref_id(player_game_ref: PlayerGameRef):
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    player_game_ref_query = create_database_query()
    try:
        existing_refs = refs.search(
            (player_game_ref_query.player_id == player_game_ref.player_id)
            & (player_game_ref_query.game_id == player_game_ref.game_id)
        )
        return existing_refs[0].doc_id if existing_refs else -1
    finally:
        db.close()


def add_ref(player_game_ref: PlayerGameRef):
    logger.info("inserting reference")
    if get_ref_id(player_game_ref) != -1:
        raise DatabaseException("reference already exists")
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    try:
        refs.insert(asdict(player_game_ref))
    finally:
        db.close()


def remove_player_refs(player_id: int):
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    player_game_ref_query = create_database_query()
    try:
        refs.remove(player_game_ref_query.player_id == player_id)
    finally:
        db.close()


def remove_game_refs(game_id: int):
    db, refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
    player_game_ref_query = create_database_query()
    try:
        refs.remove(player_game_ref_query.game_id == game_id)
    finally:
        db.close()
