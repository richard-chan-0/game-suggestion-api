import pytest
from tinydb import TinyDB
from src.database.wrapper import database_wrapper as dbw
from src.database.entities import Player, Game, PlayerGameRef


@pytest.fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"
    test_db = TinyDB(str(test_db_path))
    monkeypatch.setattr(dbw, "db", test_db)
    monkeypatch.setattr(dbw, "players", test_db.table("players"))
    monkeypatch.setattr(dbw, "games", test_db.table("games"))
    monkeypatch.setattr(dbw, "refs", test_db.table("player_game_ref"))
    yield
    test_db.close()


def test_add_player_game_ref():
    ref = PlayerGameRef(steam_id="123", app_id="g1")
    dbw.add_player_game_ref(ref)
    all_refs = dbw.refs.all()
    assert len(all_refs) == 1
    assert all_refs[0]["steam_id"] == "123"
    assert all_refs[0]["app_id"] == "g1"


def test_clean_player_games():
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g1"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g2"))
    dbw.clean_player_games("1")
    refs = dbw.refs.all()
    assert refs == []


def test_get_shared_games():
    dbw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    dbw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    dbw.add_game(Game(app_id="g1", name="TestGame"))
    dbw.add_game(Game(app_id="g2", name="TestGame 2"))
    dbw.add_game(Game(app_id="g3", name="TestGame 3"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g1"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="2", app_id="g1"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g2"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="2", app_id="g2"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g3"))

    shared = dbw.get_shared_games(["1", "2"])
    assert shared == ["TestGame", "TestGame 2"]


def test_get_shared_games_no_shared():
    dbw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    dbw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    dbw.add_game(Game(app_id="g1", name="TestGame"))
    dbw.add_game(Game(app_id="g2", name="TestGame 2"))
    dbw.add_game(Game(app_id="g3", name="TestGame 3"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g1"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="1", app_id="g2"))
    dbw.add_player_game_ref(PlayerGameRef(steam_id="2", app_id="g3"))

    shared = dbw.get_shared_games(["1", "2"])
    assert shared == []
