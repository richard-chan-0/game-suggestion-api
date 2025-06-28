# game-suggestion-api

## Overview

A Flask-based API for suggesting multiplayer games based on Steam libraries, with OpenAI integration for game recommendations.

## Features

- Add and search for players by Steam ID or name
- Refresh and store owned games for players from the Steam API
- Get shared games between players
- Get AI-powered game suggestions for a group
- Modular database layer using TinyDB

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/game-suggestion-api.git
cd game-suggestion-api
```

### 2. Install dependencies

It's recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables

Set your API keys as environment variables:

```sh
export OPENAI_KEY="your_openai_api_key"
export STEAM_API_KEY="your_steam_api_key"
```

You can also use a `.env` file in the project root:

```
OPENAI_KEY=your_openai_api_key
STEAM_API_KEY=your_steam_api_key
```

### 4. Run the API

```sh
python main.py
```

The API will be available at `http://localhost:5000/`.

## API Endpoints

### Player Endpoints

- `POST /player/`  
  Add a player.  
  **Form data:** `steam_id`, `first_name`, `last_name`

- `GET /player/`  
  Search for a player by `first_name` and `last_name` (query params).

- `GET /player/<id>`  
  Get player by internal database ID.

### Commands Endpoints

- `GET /refresh`  
  Refresh all players' owned games from Steam.

- `POST /shared`  
  Get shared games for a list of players.  
  **Form data:** `steam_ids` (list)

- `POST /suggest`  
  Get an AI-powered game suggestion for a group.  
  **Form data:** `steam_ids` (list)

## Project Structure

```
src/
  database/
    entities.py
    entity_factory.py
    wrapper/
      player_wrapper.py
      game_wrapper.py
      ref_wrapper.py
      database_wrapper.py
  lib/
    exceptions.py
    string_utils.py
  route/
    blueprints/
      player.py
      commands.py
  service/
    apis/
      steam_api_wrapper.py
      openai_api_wrapper.py
    logic/
      player.py
      commands.py
main.py
```

## Testing

Tests are located in the `tests/` directory and use `pytest`.  
To run tests:

```sh
pytest
```

## Notes

- The database uses TinyDB and stores data in `db.json` by default.
- For development/testing, the database is mocked using pytest fixtures.
- Logging is enabled for debugging.

## License

MIT License
