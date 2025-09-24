from src.database.entity_factory import create_game
from src.database.wrapper import game_wrapper
from src.apis.api_utils import create_message_response
from src.lib.exceptions import DatabaseException
import logging

logger = logging.getLogger(__name__)


def create_game(app_id: str, name: str, type: str):
    if not app_id or not name or not type:
        return create_message_response("all fields are required")

    game = create_game(app_id, name, type)
    try:
        game_wrapper.add_game(game)
    except DatabaseException as e:
        logger.error("Error adding game: %s", e)
        return create_message_response("error adding game")

    return create_message_response("game successfully added")


def search_game(name: str):
    if not name:
        return create_message_response("name is required")
    game = game_wrapper.read_game(name)
    return game if game else create_message_response("game not found")


def remove_game(name: str):
    if not name:
        return create_message_response("name is required")
    try:
        game_wrapper.remove_game(name)
    except DatabaseException as e:
        logger.error("Error removing game: %s", e)
        return create_message_response("error removing game")
    return create_message_response("game successfully removed")
