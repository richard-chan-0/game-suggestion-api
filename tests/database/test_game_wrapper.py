from pytest import fixture, raises
from tinydb import TinyDB
from src.database.wrapper import game_wrapper as gw
from src.database.entities import Game
from src.lib.exceptions import DataException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"
    test_db = TinyDB(str(test_db_path))
    monkeypatch.setattr(gw, "db", test_db)
    monkeypatch.setattr(gw, "games", test_db.table("games"))
    yield
    test_db.close()


def test_add_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    all_games = gw.games.all()
    assert len(all_games) == 1
    assert all_games[0]["name"] == "TestGame"


def test_add_duplicate_game():
    game = Game(app_id="g1", name="TestGame")
    gw.add_game(game)
    with raises(DataException):
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
    all_games = gw.games.all()
    assert all_games == []
