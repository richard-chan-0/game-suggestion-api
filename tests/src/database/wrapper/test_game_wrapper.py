from pytest import fixture, raises
from tinydb import TinyDB
from src.database.wrapper import game_wrapper as gw
from src.database.entities import Game
from src.lib.exceptions import DatabaseException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"

    # Mock the create_database_reader function to return a new TinyDB instance for each call
    def mock_create_database_reader(table_name):
        test_db = TinyDB(str(test_db_path))
        return test_db, test_db.table(table_name)

    # Apply the mock to the game_wrapper module
    monkeypatch.setattr(
        "src.database.wrapper.game_wrapper.create_database_reader",
        mock_create_database_reader,
    )


def test_add_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    all_games = gw.get_all_games()
    assert len(all_games) == 1
    assert all_games[0]["name"] == "TestGame"


def test_add_duplicate_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    with raises(DatabaseException):
        gw.add_game(game)


def test_read_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    result = gw.read_game("TestGame")
    assert result
    assert result["app_id"] == "g1"
    assert result["name"] == "TestGame"


def test_update_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    new_info = {"app_id": "g1", "name": "UpdatedGame"}
    gw.update_game("TestGame", new_info)
    updated = gw.read_game("UpdatedGame")
    assert updated


def test_remove_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    gw.remove_game("TestGame")
    all_games = gw.get_all_games()
    assert all_games == []
