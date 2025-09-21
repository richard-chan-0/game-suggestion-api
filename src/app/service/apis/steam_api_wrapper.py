from os import getenv
from requests import get
from src.app.lib.exceptions import SteamApiException, ApplicationException
from src.app.database.entity_factory import create_game_from_response


def process_response(response):
    result = response.json()
    games = result["response"]["games"]

    return [create_game_from_response(game) for game in games]


def get_owned_games(steam_id):
    steam_api_key = getenv("STEAM_API_KEY")
    if not steam_api_key:
        raise ApplicationException("STEAM_API_KEY environment variable is not set")

    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steam_api_key}&steamid={steam_id}&include_appinfo=1&format=json"

    try:
        response = get(url)
    except Exception as e:
        raise SteamApiException(f"error occurred with api: {e}")

    if response.status_code != 200:
        raise SteamApiException(f"invalid response occurred with api: {response}")

    return process_response(response)
