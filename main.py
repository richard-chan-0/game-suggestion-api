from flask import Flask, request
from dotenv import load_dotenv
from src.steam.steam_api_wrapper import get_owned_games
from src.database.database_wrapper import (
    add_player,
    get_all_players,
    add_game,
    add_player_game_ref,
    clean_player_games,
    get_shared_games,
)
from src.database.entity_factory import create_player, create_game, create_reference
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

load_dotenv()


@app.errorhandler(Exception)
def general_exception_handler(e):
    return str(e), 500


@app.route("/")
def home():
    return "api is running", 200


@app.route("/add-player", methods=["POST"])
def ready_player():
    steam_id = request.form.get("steam_id")
    first_name = request.form.get("first_name").lower()
    last_name = request.form.get("last_name").lower()

    player = create_player(steam_id, first_name, last_name)
    add_player(player)
    return "player successfully added", 200


@app.route("/refresh", methods=["GET"])
def refresh_shared_games():
    steam_ids = get_all_players()
    for id in steam_ids:
        clean_player_games(id)
        games = get_owned_games(id)
        for app_id, game_name in games:
            add_game(create_game(app_id, game_name))
            add_player_game_ref(create_reference(id, app_id))
    return "table refreshed", 200


@app.route("/shared", methods=["POST"])
def get_shared_games():
    steam_ids = request.form.getlist("steam_ids")
    games = get_shared_games(steam_ids), 200
    if games:
        return games, 200
    else:
        return "no shared games", 200


app.run(debug=True)
