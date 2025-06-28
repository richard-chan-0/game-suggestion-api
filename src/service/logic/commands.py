"""
grpc, command specific api logic
"""

from src.database.wrapper import database_wrapper
from src.service.apis.openai_api_wrapper import get_suggestion


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
