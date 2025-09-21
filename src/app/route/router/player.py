from fastapi import APIRouter, Request
from logging import getLogger
from src.app.service.logic.player import *

logger = getLogger(__name__)
player_router = APIRouter()


@player_router.get("")
def index(first_name: str, last_name: str):
    logger.info("Searching player by name: %s %s", first_name, last_name)
    return search_player(first_name, last_name)


@player_router.post("")
def add_player(request: Request):
    return ready_player(request)


@player_router.get("/<int:id>")
def get_player(id: int):
    return search_player_by_id(id)
