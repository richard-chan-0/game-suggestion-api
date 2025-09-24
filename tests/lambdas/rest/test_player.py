import pytest
from lambdas.rest.player import ready_player, search_player, search_player_by_id
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_player_wrapper():
    with patch("lambdas.rest.player.player_wrapper") as mock_wrapper:
        yield mock_wrapper


@pytest.fixture
def mock_create_player():
    with patch("lambdas.rest.player.create_player") as mock_create:
        yield mock_create


@pytest.fixture
def mock_create_message_response():
    with patch("lambdas.rest.player.create_message_response") as mock_response:
        yield mock_response


def test_ready_player(
    mock_player_wrapper, mock_create_player, mock_create_message_response
):
    mock_create_player.return_value = MagicMock()
    mock_create_message_response.return_value = "player successfully added"

    response = ready_player("12345", "John", "Doe")

    mock_create_player.assert_called_once_with("12345", "John", "Doe")
    mock_player_wrapper.add_player.assert_called_once()
    assert response == "player successfully added"


def test_search_player_found(mock_player_wrapper, mock_create_message_response):
    mock_player_wrapper.read_player_by_name.return_value = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
    }

    response = search_player("John", "Doe")

    mock_player_wrapper.read_player_by_name.assert_called_once_with("John", "Doe")
    assert response == {"id": 1, "first_name": "John", "last_name": "Doe"}


def test_search_player_not_found(mock_player_wrapper, mock_create_message_response):
    mock_player_wrapper.read_player_by_name.return_value = None
    mock_create_message_response.return_value = "player not found"

    response = search_player("John", "Doe")

    mock_player_wrapper.read_player_by_name.assert_called_once_with("John", "Doe")
    mock_create_message_response.assert_called_once_with("player not found")
    assert response == "player not found"


def test_search_player_by_id_found(mock_player_wrapper, mock_create_message_response):
    mock_player_wrapper.get_player_by_id.return_value = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
    }

    response = search_player_by_id(1)

    mock_player_wrapper.get_player_by_id.assert_called_once_with(1)
    assert response == {"id": 1, "first_name": "John", "last_name": "Doe"}


def test_search_player_by_id_not_found(
    mock_player_wrapper, mock_create_message_response
):
    mock_player_wrapper.get_player_by_id.return_value = None
    mock_create_message_response.return_value = "player not found"

    response = search_player_by_id(1)

    mock_player_wrapper.get_player_by_id.assert_called_once_with(1)
    mock_create_message_response.assert_called_once_with("player not found")
    assert response == "player not found"
