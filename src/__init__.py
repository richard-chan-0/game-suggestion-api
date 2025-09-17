from flask import Flask
from src.app.route import blueprints

app = Flask("game_suggestion_api")
app.register_blueprint(blueprints.player_blueprint)
app.register_blueprint(blueprints.commands_blueprint)


@app.errorhandler(Exception)
def general_exception_handler(e):
    return str(e), 500


@app.route("/")
def home():
    return "api is running", 200
