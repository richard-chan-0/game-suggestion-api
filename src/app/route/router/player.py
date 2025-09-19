from fastapi import APIRouter, Request
from src.app.service.logic.player import *

player_router = APIRouter()


@player_router.get("")
async def index(first_name: str, last_name: str):
    return await search_player(first_name, last_name)


@player_router.post("")
async def ready_player(request: Request):
    return await ready_player(request)


@player_router.get("/<int:id>")
async def get_player(id: int):
    return await search_player_by_id(id)
