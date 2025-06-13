from src.database.wrapper.player_wrapper import *
from src.database.wrapper.game_wrapper import *
from src.database.wrapper.ref_wrapper import *


def get_shared_games(steam_ids: list[str]):
    player_game_refs = refs.search(PlayerGameRefQuery.steam_id.one_of(steam_ids))
    if not player_game_refs:
        raise DataException("no data found")
    all_games = {}
    for ref in player_game_refs:
        app_id = ref["app_id"]
        steam_id = ref["steam_id"]
        if app_id not in all_games:
            all_games[app_id] = [steam_id]
        else:
            all_games[app_id].append(steam_id)

    shared_ids = [
        app_id
        for app_id, players in all_games.items()
        if len(players) == len(steam_ids)
    ]

    shared_games = games.search(GameQuery.app_id.one_of(shared_ids))
    return [game["name"] for game in shared_games]
