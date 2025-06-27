from flask import Blueprint, request
from src.route.logic.player import *

player_blueprint = Blueprint("player", __name__)


@player_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return ready_player(request)
    elif request.method == "GET":
        return search_player(request)
    else:
        return "unsupported method", 400


@player_blueprint.route("/<int:id>", methods=["GET"])
def get_player(id):
    return "get player", 200
