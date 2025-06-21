from src.database.entity_factory import create_player
from src.database.wrapper import database_wrapper
from src.apis.openai_api_wrapper import get_suggestion
import logging

logger = logging.getLogger(__name__)


def ready_player(request):
    steam_id = request.form.get("steam_id")
    first_name = request.form.get("first_name").lower()
    last_name = request.form.get("last_name").lower()

    player = create_player(steam_id, first_name, last_name)
    database_wrapper.player_wrapper.add_player(player)
    return "player successfully added", 200


def refresh_shared_games():
    database_wrapper.refresh_shared_games()
    return "table refreshed", 200


def get_shared_games(request):
    steam_ids = request.form.getlist("steam_ids")
    games = database_wrapper.get_shared_games(steam_ids)
    if games:
        return games, 200
    else:
        return "no shared games", 200


def suggest_games(request):
    steam_ids = request.form.getlist("steam_ids")
    games = database_wrapper.get_shared_games(steam_ids)
    if not games:
        return "no shared games", 200

    game = get_suggestion(games, len(steam_ids))
    if game:
        return game, 200
    else:
        return "no suggestion", 200
