from pytest import fixture, raises
from tinydb import TinyDB
from src.database.wrapper import ref_wrapper as rw
from src.database.entities import PlayerGameRef
from src.lib.exceptions import DataException


@fixture(autouse=True)
def setup_db(monkeypatch, tmp_path):
    test_db_path = tmp_path / "test_db.json"
    test_db = TinyDB(str(test_db_path))
    monkeypatch.setattr(rw, "db", test_db)
    monkeypatch.setattr(rw, "refs", test_db.table("player_ref_ref"))
    yield
    test_db.close()


def test_add_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    all_refs = rw.refs.all()
    assert len(all_refs) == 1
    assert all_refs[0] == {"player_id": 1, "game_id": 1}


def test_add_duplicate_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    with raises(DataException):
        rw.add_ref(new_ref)


def test_read_ref():
    new_ref = PlayerGameRef(player_id=1, game_id=1)
    rw.add_ref(new_ref)
    result = rw.get_ref_id(new_ref)
    assert result
