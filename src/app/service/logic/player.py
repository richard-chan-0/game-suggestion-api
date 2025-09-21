from src.app.database.entity_factory import create_player
from src.app.database.wrapper import player_wrapper
from src.app.lib.api_utils import create_message_response
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
