from pytest import fixture
from tinydb import TinyDB
from src.database.wrapper import (
    database_wrapper as dw,
    player_wrapper as pw,
    game_wrapper as gw,
    ref_wrapper as rw,
)
from src.database.entities import Player, Game, PlayerGameRef


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"
    test_db = TinyDB(str(test_db_path))
    monkeypatch.setattr(pw, "players", test_db.table("players"))
    monkeypatch.setattr(gw, "games", test_db.table("games"))
    monkeypatch.setattr(rw, "refs", test_db.table("player_game_ref"))

    yield
    test_db.close()


def test_get_shared_games():
    player_id1 = pw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    player_id2 = pw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    game_id1 = gw.add_game(Game(app_id="g1", name="TestGame"))
    game_id2 = gw.add_game(Game(app_id="g2", name="TestGame 2"))
    game_id3 = gw.add_game(Game(app_id="g3", name="TestGame 3"))
    rw.add_ref(PlayerGameRef(player_id=player_id1, game_id=game_id1))
    rw.add_ref(PlayerGameRef(player_id=player_id2, game_id=game_id1))
    rw.add_ref(PlayerGameRef(player_id=player_id1, game_id=game_id2))
    rw.add_ref(PlayerGameRef(player_id=player_id2, game_id=game_id2))
    rw.add_ref(PlayerGameRef(player_id=player_id1, game_id=game_id3))

    shared = dw.get_shared_games(["1", "2"])
    assert shared == ["TestGame", "TestGame 2"]


def test_get_shared_games_no_shared():
    player_id1 = pw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    player_id2 = pw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    game_id1 = gw.add_game(Game(app_id="g1", name="TestGame"))
    game_id2 = gw.add_game(Game(app_id="g2", name="TestGame 2"))
    game_id3 = gw.add_game(Game(app_id="g3", name="TestGame 3"))
    rw.add_ref(PlayerGameRef(player_id=player_id1, game_id=game_id1))
    rw.add_ref(PlayerGameRef(player_id=player_id2, game_id=game_id2))
    rw.add_ref(PlayerGameRef(player_id=player_id1, game_id=game_id3))

    shared = dw.get_shared_games(["1", "2"])
    assert shared == []
