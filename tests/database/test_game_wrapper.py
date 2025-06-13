from pytest import fixture
from tinydb import TinyDB
from src.database.wrapper import game_wrapper as gw
from src.database.entities import Game


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
