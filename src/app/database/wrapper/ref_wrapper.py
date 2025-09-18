from tinydb import TinyDB, Query
from dataclasses import asdict
from src.app.database.entities import *
from src.app.lib.exceptions import DataException
from src.app.database.constants import PLAYER_GAME_REF_TABLE_NAME
from src.app.database.entity_factory import (
    create_database_query,
    create_database_reader,
)
import logging

logger = logging.getLogger(__name__)

refs = create_database_reader(PLAYER_GAME_REF_TABLE_NAME)
PlayerGameRefQuery = create_database_query()


def get_refs_for_players(player_ids: list[int]):
    return refs.search(PlayerGameRefQuery.player_id.one_of(player_ids))


def get_refs_for_player(player_id: int):
    return refs.search(PlayerGameRef.player_id == player_id)


def get_ref_id(player_game_ref: PlayerGameRef):
    existing_refs = refs.search(
        (PlayerGameRefQuery.player_id == player_game_ref.player_id)
        & (PlayerGameRefQuery.game_id == player_game_ref.game_id)
    )
    return existing_refs[0].doc_id if existing_refs else -1


def add_ref(player_game_ref: PlayerGameRef):
    logger.info("inserting reference")
    if get_ref_id(player_game_ref) != -1:
        raise DataException("reference already exists")
    refs.insert(asdict(player_game_ref))


def remove_player_refs(player_id: int):
    refs.remove(PlayerGameRefQuery.player_id == player_id)


def remove_game_refs(game_id: int):
    refs.remove(PlayerGameRefQuery.game_id == game_id)
