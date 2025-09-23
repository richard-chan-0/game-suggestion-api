"""
grpc style command specific api logic
"""

from logging import getLogger
from src.database.wrapper import player_wrapper, ref_wrapper, game_wrapper
from src.lib.exceptions import DatabaseException

logger = getLogger(__name__)


def process_refs_and_get_shared_games(player_game_refs, steam_ids):
    all_games = {}
    for ref in player_game_refs:
        game_id = ref["game_id"]
        player_id = ref["player_id"]
        if game_id not in all_games:
            all_games[game_id] = [player_id]
        else:
            all_games[game_id].append(player_id)

    return [
        game_id
        for game_id, player_id in all_games.items()
        if len(steam_ids) == len(player_id)
    ]


def get_shared_games(steam_ids: list[str]):
    logger.info("getting shared games for players")
    player_ids = [player_wrapper.get_player_id(steam_id) for steam_id in steam_ids]
    player_game_refs = ref_wrapper.get_refs_for_players(player_ids)
    if not player_game_refs:
        raise DatabaseException("no data found")

    shared_ids = process_refs_and_get_shared_games(player_game_refs, steam_ids)
    shared_games = [game_wrapper.get_game(game_id) for game_id in shared_ids]
    return [game["name"] for game in shared_games]
