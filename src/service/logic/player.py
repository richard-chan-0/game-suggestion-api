from src.database.entity_factory import create_player
from src.database.wrapper import database_wrapper
from src.service.apis.openai_api_wrapper import get_suggestion
import logging

logger = logging.getLogger(__name__)


def ready_player(request):
    steam_id = request.form.get("steam_id")
    first_name = request.form.get("first_name").lower()
    last_name = request.form.get("last_name").lower()

    player = create_player(steam_id, first_name, last_name)
    database_wrapper.player_wrapper.add_player(player)
    return "player successfully added", 200


def search_player(request):
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    if not first_name or not last_name:
        return "first name and last name are required", 400
    player = database_wrapper.player_wrapper.read_player_by_name(
        first_name.lower(), last_name.lower()
    )
    return player if player else "player not found", 200


def search_player_by_id(id):
    player = database_wrapper.player_wrapper.get_player_by_id(id)
    return player if player else "player not found", 200
