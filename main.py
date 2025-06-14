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
    # TODO: refs for multiple users not created
    # TODO: game names have special characters
    return route_logic.refresh_shared_games()


@app.route("/shared", methods=["POST"])
def get_shared_games():
    return route_logic.get_shared_games(request)


app.run(debug=True)
