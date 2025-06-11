from flask import Flask, request
from dotenv import load_dotenv
from src.steam.steam_api_wrapper import get_owned_games
from src.database.database_wrapper import (
    add_player,
    get_all_players,
    add_game,
    add_player_game_ref,
    clean_player_games,
)
from src.database.entity_factory import create_player, create_game, create_reference
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

load_dotenv()


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
    # because this is made as a simple api I don't want to put the time and effort to
    # set up a database so having a simple file that can be updated regularly should
    # be sufficient to keep track of who has what game
    # TODO: read from a json file each read
    pass


app.run(debug=True)
