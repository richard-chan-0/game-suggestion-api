from flask import Flask
from dotenv import load_dotenv
from src.route import blueprints
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprints.player_blueprint)
app.register_blueprint(blueprints.commands_blueprint)

load_dotenv()


@app.errorhandler(Exception)
def general_exception_handler(e):
    return str(e), 500


@app.route("/")
def home():
    return "api is running", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
