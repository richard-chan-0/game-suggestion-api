from src.database.wrapper import player_wrapper, game_wrapper, ref_wrapper
from src.lib.exceptions import DataException
from src.database.entity_factory import create_game, create_reference
from src.database.entities import Game
from src.steam.steam_api_wrapper import get_owned_games
import logging

logger = logging.getLogger(__name__)


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
        raise DataException("no data found")

    shared_ids = process_refs_and_get_shared_games(player_game_refs, steam_ids)
    shared_games = [game_wrapper.get_game(game_id) for game_id in shared_ids]
    return [game["name"] for game in shared_games]


def get_game_id(app_id: str, game_name: str):
    game_id = game_wrapper.get_game_id(game_name)

    return (
        game_wrapper.add_game(create_game(app_id, game_name))
        if game_id == -1
        else game_id
    )


def refresh_player_games(player, games: list[Game]):
    logger.info(
        "refreshing games for player %s",
        f"{player['first_name']} {player['last_name']}",
    )
    for game in games:
        game_id = get_game_id(game.app_id, game.name)
        ref_id = ref_wrapper.get_ref_id(create_reference(player.doc_id, game_id))
        if ref_id == -1:
            ref_wrapper.add_ref(create_reference(player.doc_id, game_id))


def refresh_shared_games():
    logger.info("refreshing owned games for all players")
    players = player_wrapper.get_all_players()
    for player in players:
        id = player["steam_id"]
        games = get_owned_games(id)
        refresh_player_games(player, games)
