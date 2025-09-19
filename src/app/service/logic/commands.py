"""
grpc, command specific api logic
"""

from logging import getLogger
from src.app.database.wrapper import database_wrapper
from src.app.service.apis.openai_api_wrapper import get_suggestion

logger = getLogger(__name__)


async def refresh_shared_games():
    database_wrapper.refresh_shared_games()
    return "table refreshed", 200


async def get_shared_games(steam_ids: list[str]):
    games = await database_wrapper.get_shared_games(steam_ids)
    if games:
        return games, 200
    else:
        return "no shared games", 200


async def suggest_games(steam_ids: list[str]):
    games = await database_wrapper.get_shared_games(steam_ids)
    if not games:
        return "no shared games", 200

    logger.info("games shared by players: %s", games)

    game = await get_suggestion(games, len(steam_ids))
    if game:
        return game, 200
    else:
        return "no suggestion", 200
