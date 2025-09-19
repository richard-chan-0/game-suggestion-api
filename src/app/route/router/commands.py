from fastapi import APIRouter, Request
from src.app.service.logic.commands import (
    refresh_shared_games,
    get_shared_games,
    suggest_games,
)

commands_router = APIRouter()


@commands_router.get("/refresh")
async def get_refresh_shared_games():
    return await refresh_shared_games()


@commands_router.post("/shared")
async def get_shared_games_for_players(request: Request):
    return await get_shared_games(request)


@commands_router.post("/suggest")
async def get_game_suggestion(request: Request):
    return await suggest_games(request)
