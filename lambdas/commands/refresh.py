from logging import getLogger
from src.database.entities import Game
from src.database.entity_factory import create_game, create_reference
from src.database.wrapper import ref_wrapper, game_wrapper

logger = getLogger(__name__)


def get_game_id(app_id: str, game_name: str):
    """
    Get the game ID from the database, or add it if it does not exist.
    """
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
