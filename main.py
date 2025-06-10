from flask import Flask, request
from dotenv import load_dotenv
from src.steam_api_wrapper import get_owned_games

app = Flask(__name__)

load_dotenv()


@app.route("/")
def home():
    return "api is running", 200


@app.route("/refresh", methods=["GET"])
def refresh_shared_games():
    # TODO: read from steam api for set of steam users and add to list of users and there games
    get_owned_games()
    pass


@app.route("/shared", methods=["POST"])
def get_shared_games():
    # because this is made as a simple api I don't want to put the time and effort to
    # set up a database so having a simple file that can be updated regularly should
    # be sufficient to keep track of who has what game
    # TODO: read from a json file each read
    pass


app.run()
