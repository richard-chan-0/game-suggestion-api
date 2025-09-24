from logging import getLogger
from handler import (
    refresh_shared_games,
    get_shared_games_for_all_players,
    get_shared_games_for_steam_ids,
    suggest_games_for_all_players,
    suggest_games,
)

logger = getLogger(__name__)


def process_gets(event):
    path = event.get("path")

    if path == "/refresh":
        return refresh_shared_games()
    elif path == "/shared":
        return get_shared_games_for_all_players()
    elif path == "/suggest":
        return suggest_games_for_all_players()

    return {
        "statusCode": 400,
        "body": "Invalid GET request path",
    }


def process_posts(event):
    path = event.get("path")
    body = event.get("body", {})

    if path == "/shared":
        steam_ids = body.get("steam_ids", [])
        if steam_ids:
            return get_shared_games_for_steam_ids(steam_ids)
        else:
            return {
                "statusCode": 400,
                "body": "Missing 'steam_ids' in request body",
            }
    elif path == "/suggest":
        steam_ids = body.get("steam_ids", [])
        if steam_ids:
            return suggest_games(steam_ids)
        else:
            return {
                "statusCode": 400,
                "body": "Missing 'steam_ids' in request body",
            }
    return {
        "statusCode": 400,
        "body": "Invalid POST request path",
    }


def event_controller(event):
    """
    Process incoming events and route them to the appropriate handler.
    """
    method = event.get("httpMethod")

    if method == "GET":
        return process_gets(event)

    elif method == "POST":
        return process_posts(event)
