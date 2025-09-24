from src.lib.exceptions import DatabaseException
from src.database.entity_factory import create_player
from src.database.wrapper import player_wrapper
from src.apis.api_utils import create_message_response
import logging

logger = logging.getLogger(__name__)


def ready_player(steam_id: str, first_name: str, last_name: str):
    player = create_player(steam_id, first_name, last_name)
    player_wrapper.add_player(player)
    return create_message_response("player successfully added")


def search_player(first_name: str, last_name: str):
    if not first_name or not last_name:
        return create_message_response("first name and last name are required")
    player = player_wrapper.read_player_by_name(first_name, last_name)
    return player if player else create_message_response("player not found")


def search_player_by_id(id):
    player = player_wrapper.get_player_by_id(id)
    return player if player else create_message_response("player not found")


def remove_player(steam_id: str):
    if not steam_id:
        return create_message_response("steam id is required")
    try:
        player_wrapper.remove_player(steam_id)
    except DatabaseException as e:
        logger.error("Error removing player: %s", e)
        return create_message_response("error removing player")
    return create_message_response("player successfully removed")
