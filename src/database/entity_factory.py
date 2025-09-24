from os import getenv
from src.database.entities import *
from src.lib.string_utils import clean_name
from src.database.constants import DEV_DATABASE_PATH, PROD_DATABASE_PATH
from tinydb import TinyDB, Query
from tinydb.table import Table
from logging import getLogger

logger = getLogger(__name__)


def create_player(steam_id, first_name, last_name):
    return Player(steam_id, first_name, last_name)


def create_game(app_id, name):
    return Game(app_id, name)


def create_game_from_response(response):
    app_id = response["appid"]
    name = clean_name(response["name"])
    return create_game(app_id, name)


def create_reference(steam_id, app_id):
    return PlayerGameRef(steam_id, app_id)


def create_database_reader(table_name: str) -> tuple[TinyDB, Table]:
    """
    Create a TinyDB reader for the specified table.
    Uses different database files based on the TINYDB_BUCKET environment variable.
    """
    is_production = bool(getenv("TINYDB_BUCKET", ""))
    db_path = PROD_DATABASE_PATH if is_production else DEV_DATABASE_PATH
    db = TinyDB(db_path)
    table = db.table(table_name)
    return db, table


def create_database_query():
    return Query()
