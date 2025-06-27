from flask import Flask, request
from dotenv import load_dotenv
from src.route.blueprints import player_blueprint
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

load_dotenv()


@app.errorhandler(Exception)
def general_exception_handler(e):
    return str(e), 500


@app.register_blueprint(player_blueprint)
@app.route("/")
def home():
    return "api is running", 200


# TODO: create a endpoint for player entity /player /player/:id/refresh
# TODO: create a endpoint for game entity
# TODO: figure out grpc related endpoints besides suggest
# TODO: refactor main?


@app.route("/player")
def player(id):
    method = request.method
    if method == "POST":
        return ready_player(request)
    if method == "GET":
        return "get player", 200
    return "unsupported method", 400


@app.route("/refresh", methods=["GET"])
def refresh_shared_games():
    return refresh_shared_games()


@app.route("/shared", methods=["POST"])
def get_shared_games():
    return get_shared_games(request)


@app.route("suggest", methods=["POST"])
def suggest_games():
    return suggest_games(request)


app.run(debug=True)
