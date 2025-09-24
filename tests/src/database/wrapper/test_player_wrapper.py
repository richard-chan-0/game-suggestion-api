from pytest import fixture, raises
from src.database.wrapper import player_wrapper as pw
from src.database.entities import Player
from tinydb import TinyDB
from src.lib.exceptions import DatabaseException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"

    # Mock the create_database_reader function to return a new TinyDB instance for each call
    def mock_create_database_reader(table_name):
        test_db = TinyDB(str(test_db_path))
        return test_db, test_db.table(table_name)

    # Apply the mock to the player_wrapper module
    monkeypatch.setattr(
        "src.database.wrapper.player_wrapper.create_database_reader",
        mock_create_database_reader,
    )


def test_add_and_read_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    result = pw.read_player("123")
    assert result
    assert result["steam_id"] == "123"
    assert result["first_name"] == "test"
    assert result["last_name"] == "user"


def test_add_player_duplicate():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    with raises(DatabaseException):
        pw.add_player(player)


def test_remove_player():
    player = Player(steam_id="123", first_name="test", last_name="user")
    pw.add_player(player)
    pw.remove_player("123")
    all_players = pw.get_all_players()
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
    assert updated_player == {**new_info, "last_name": "user"}


def test_get_all_players():
    pw.add_player(Player(steam_id="1", first_name="A", last_name="Z"))
    pw.add_player(Player(steam_id="2", first_name="B", last_name="Y"))
    players = pw.get_all_players()
    assert len(players) == 2
