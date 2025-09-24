from logging import getLogger
from refresh import refresh_player_games
from shared import get_shared_games
from apis.openai_api_wrapper import get_suggestion
from apis.steam_api_wrapper import get_owned_games
from src.apis.api_utils import create_message_response
from src.database.wrapper import player_wrapper

logger = getLogger(__name__)


def refresh_shared_games():
    logger.info("refreshing owned games for all players")
    players = player_wrapper.get_all_players()
    for player in players:
        logger.info("refreshing games for player %s", player["steam_id"])
        games = get_owned_games(player["steam_id"])
        refresh_player_games(player, games)
    return create_message_response("table refreshed")


def get_shared_games_for_all_players():
    players = player_wrapper.get_all_players()
    steam_ids = [player["steam_id"] for player in players]
    return get_shared_games_for_steam_ids(steam_ids)


def get_shared_games_for_steam_ids(steam_ids: list[str]):
    games = get_shared_games(steam_ids)
    if games:
        return {"games": games}
    else:
        return create_message_response("no shared games")


def suggest_games_for_all_players():
    players = player_wrapper.get_all_players()
    steam_ids = [player["steam_id"] for player in players]
    return suggest_games(steam_ids)


def suggest_games(steam_ids: list[str]):
    games = get_shared_games(steam_ids)
    if not games:
        return create_message_response("no shared games")

    logger.info("games shared by players: %s", games)

    suggestions = get_suggestion(games, len(steam_ids))
    if suggestions:
        return {"suggestions": suggestions}
    else:
        return create_message_response("no suggestion")
