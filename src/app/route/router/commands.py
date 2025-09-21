from fastapi import APIRouter
from pydantic import BaseModel
from src.app.service.logic.commands import (
    refresh_shared_games,
    get_shared_games_for_steam_ids,
    suggest_games,
)

commands_router = APIRouter()


class CommandRequest(BaseModel):
    steam_ids: list[str]


@commands_router.get("/refresh")
def refresh_players_shared_games():
    return refresh_shared_games()


@commands_router.post("/shared")
def shared_games_for_players(request: CommandRequest):
    steam_ids = request.steam_ids
    return get_shared_games_for_steam_ids(steam_ids)


@commands_router.post("/suggest")
def suggest_game_suggestion(request: CommandRequest):
    steam_ids = request.steam_ids
    return suggest_games(steam_ids)
