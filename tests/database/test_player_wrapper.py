from pytest import fixture, raises
from src.database.wrapper import player_wrapper as pw
from src.database.entities import Player
from tinydb import TinyDB
from src.lib.exceptions import DataException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"
    test_db = TinyDB(str(test_db_path))
    monkeypatch.setattr(pw, "db", test_db)
    monkeypatch.setattr(pw, "players", test_db.table("players"))
    yield
    test_db.close()


def test_add_and_read_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    result = pw.read_player("123")
    assert result
    assert result["steam_id"] == "123"
    assert result["first_name"] == "test"
    assert result["last_name"] == "user"


def test_add_player_duplicate():
    """
    insert a duplicate player scenario, no duplicates should be inserted
    """
    with raises(DataException):
        player = Player(steam_id="123", first_name="test", last_name="user")
        pw.add_player(player)
        pw.add_player(player)
        all_players = pw.players.all()
        assert len(all_players) == 1


def test_remove_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    pw.remove_player("123")
    all_players = pw.players.all()
    assert not all_players


def test_get_player_id():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    player_id = pw.get_player_id("123")
    assert player_id == 1


def test_update_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    new_info = {"steam_id": "789", "first_name": "updated_test"}
    pw.update_player("123", new_info)
    updated_player = pw.read_player("789")
    assert len(pw.get_all_players()) == 1
    print(updated_player)
    print({**new_info, "last_name": "user"})
    assert updated_player == {**new_info, "last_name": "user"}


def test_get_all_players():
    pw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    pw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    ids = pw.get_all_players()
    assert set(ids) == {1, 2}
