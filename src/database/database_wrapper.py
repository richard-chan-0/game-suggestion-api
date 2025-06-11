from tinydb import TinyDB, Query
from dataclasses import asdict
from src.database.entities import *
from src.lib.exceptions import DataException
import logging

logger = logging.getLogger(__name__)

db = TinyDB("db.json")
players = db.table("players")
games = db.table("games")
refs = db.table("player_game_ref")

PlayerQuery = Query()
GameQuery = Query()
PlayerGameRefQuery = Query()


def read_player(steam_id: str):
    logger.info("finding player")
    return players.search(PlayerQuery.steam_id == steam_id)


def add_player(player: Player):
    logger.info("inserting new player")
    existing_player = read_player(player.steam_id)
    if existing_player:
        logger.info("existing player found")
        return

    p = asdict(player)
    players.insert(p)


def add_game(game: Game):
    logger.info("inserting new game: %s", game.name)
    games.insert(asdict(game))


def add_player_game_ref(player_game_ref: PlayerGameRef):
    logger.info("inserting reference")
    refs.insert(asdict(player_game_ref))


def get_all_players():
    return [Player(**player).steam_id for player in players.all()]


def clean_player_games(steam_id: str):
    refs.remove(PlayerGameRefQuery.steam_id == steam_id)


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
