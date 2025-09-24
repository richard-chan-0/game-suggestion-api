from pytest import fixture, raises
from tinydb import TinyDB
from src.database.wrapper import ref_wrapper as rw
from src.database.entities import PlayerGameRef
from src.lib.exceptions import DatabaseException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"

    # Mock the create_database_reader function to return a new TinyDB instance for each call
    def mock_create_database_reader(table_name):
        test_db = TinyDB(str(test_db_path))
        return test_db, test_db.table(table_name)

    # Apply the mock to the ref_wrapper module
    monkeypatch.setattr(
        "src.database.wrapper.ref_wrapper.create_database_reader",
        mock_create_database_reader,
    )


def test_add_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    all_refs = rw.get_all_refs()
    assert len(all_refs) == 1
    assert all_refs[0] == {"player_id": 1, "game_id": 1}


def test_add_duplicate_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    with raises(DatabaseException):
        rw.add_ref(new_ref)


def test_read_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    result = rw.get_ref_id(new_ref)
    assert result
