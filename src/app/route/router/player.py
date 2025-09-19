from fastapi import APIRouter, Request
from logging import getLogger
from src.app.service.logic.player import *

logger = getLogger(__name__)
player_router = APIRouter()


@player_router.get("")
async def index(first_name: str, last_name: str):
    logger.info("Searching player by name: %s %s", first_name, last_name)
    return await search_player(first_name, last_name)


@player_router.post("")
async def ready_player(request: Request):
    return await ready_player(request)


@player_router.get("/<int:id>")
async def get_player(id: int):
    return await search_player_by_id(id)
