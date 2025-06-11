import pytest
from tinydb import TinyDB
from src.database import database_wrapper as dbw
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


def test_add_and_read_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    dbw.add_player(player)
    result = dbw.read_player("123")
    assert result
    assert result[0]["steam_id"] == "123"
    assert result[0]["first_name"] == "test"
    assert result[0]["last_name"] == "user"


def test_add_player_duplicate():
    player = Player(steam_id="123", first_name="test", last_name="user")
    dbw.add_player(player)
    dbw.add_player(player)  # Should not insert duplicate
    all_players = dbw.players.all()
    assert len(all_players) == 1


def test_add_game():
    game = Game(app_id="g1", name="TestGame")
    dbw.add_game(game)
    all_games = dbw.games.all()
    assert len(all_games) == 1
    assert all_games[0]["name"] == "TestGame"


def test_add_player_game_ref():
    ref = PlayerGameRef(steam_id="123", app_id="g1")
    dbw.add_player_game_ref(ref)
    all_refs = dbw.refs.all()
    assert len(all_refs) == 1
    assert all_refs[0]["steam_id"] == "123"
    assert all_refs[0]["app_id"] == "g1"


def test_get_all_players():
    dbw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    dbw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    ids = dbw.get_all_players()
    assert set(ids) == {"1", "2"}


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
