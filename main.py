from flask import Flask, request
from dotenv import load_dotenv
from src import route_logic
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
    return route_logic.ready_player(request)


@app.route("/refresh", methods=["GET"])
def refresh_shared_games():
    # steam_ids = get_all_players()
    # for id in steam_ids:
    #     clean_player_games(id)
    #     games = get_owned_games(id)
    #     for app_id, game_name in games:
    #         add_game(create_game(app_id, game_name))
    #         add_player_game_ref(create_reference(id, app_id))
    # return "table refreshed", 200
    pass


@app.route("/shared", methods=["POST"])
def get_shared_games():
    return route_logic.get_shared_games(request)


app.run(debug=True)
