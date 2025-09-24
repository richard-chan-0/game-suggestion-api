import pytest
from lambdas.rest.game import create_game, search_game, remove_game
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_game_wrapper():
    with patch("lambdas.rest.game.game_wrapper") as mock_wrapper:
        yield mock_wrapper


@pytest.fixture
def mock_create_game():
    with patch("lambdas.rest.game.create_game") as mock_create:
        yield mock_create


@pytest.fixture
def mock_create_message_response():
    with patch("lambdas.rest.game.create_message_response") as mock_response:
        yield mock_response


def test_add_game(mock_game_wrapper, mock_create_game, mock_create_message_response):
    mock_create_game.return_value = MagicMock()
    mock_create_message_response.return_value = "game successfully added"

    response = create_game("12345", "Chess", "Board Game")

    mock_create_game.assert_called_once_with("12345", "Chess", "Board Game")
    mock_game_wrapper.add_game.assert_called_once()
    assert response == "game successfully added"


def test_search_game_found(mock_game_wrapper):
    mock_game_wrapper.read_game.return_value = {
        "id": 1,
        "name": "Chess",
        "type": "Board Game",
    }

    response = search_game("Chess")

    mock_game_wrapper.read_game.assert_called_once_with("Chess")
    assert response == {"id": 1, "name": "Chess", "type": "Board Game"}


def test_search_game_not_found(mock_game_wrapper, mock_create_message_response):
    mock_game_wrapper.read_game.return_value = None
    mock_create_message_response.return_value = "game not found"

    response = search_game("Chess")

    mock_game_wrapper.read_game.assert_called_once_with("Chess")
    mock_create_message_response.assert_called_once_with("game not found")
    assert response == "game not found"
