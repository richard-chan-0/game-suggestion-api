from flask import Blueprint, request
from src.service.logic.commands import (
    refresh_shared_games,
    get_shared_games,
    suggest_games,
)

commands_blueprint = Blueprint("commands", __name__)


@commands_blueprint.route("/refresh", methods=["GET"])
def get_refresh_shared_games():
    return refresh_shared_games()


@commands_blueprint.route("/shared", methods=["POST"])
def get_shared_games():
    return get_shared_games(request)


@commands_blueprint.route("/suggest", methods=["POST"])
def get_game_suggestion():
    return suggest_games(request)
