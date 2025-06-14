from src.database.entity_factory import create_player, create_game, create_reference
from src.database.wrapper import database_wrapper
from src.steam.steam_api_wrapper import get_owned_games
from src.lib.exceptions import DataException
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
    players = database_wrapper.player_wrapper.get_all_players()
    for player in players:
        id = player["steam_id"]
        games = get_owned_games(id)
        for app_id, game_name in games:
            try:
                game_id = database_wrapper.game_wrapper.add_game(
                    create_game(app_id, game_name)
                )
            except DataException:
                logger.info("game %s already exists, skipped from refresh", game_name)
                continue
            database_wrapper.ref_wrapper.add_ref(
                create_reference(player.doc_id, game_id)
            )
    return "table refreshed", 200


def get_shared_games(request):
    steam_ids = request.form.getlist("steam_ids")
    games = database_wrapper.get_shared_games(steam_ids), 200
    if games:
        return games, 200
    else:
        return "no shared games", 200
