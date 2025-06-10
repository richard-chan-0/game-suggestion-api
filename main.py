from flask import Flask
from dotenv import load_dotenv
from src.steam_api_wrapper import get_owned_games

app = Flask(__name__)

load_dotenv()


@app.route("/")
def home():
    return get_owned_games(), 200


app.run()
