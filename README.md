# game-suggestion-api

## Overview

A Flask-based API for suggesting multiplayer games based on Steam libraries, with OpenAI integration for game recommendations.

## Features

- Add and search for players by Steam ID or name
- Refresh and store owned games for players from the Steam API
- Get shared games between players
- Get AI-powered game suggestions for a group
- Modular database layer using TinyDB

## Setup (Local Development)

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

### 4. Run the API Locally

```sh
python main.py
```

The API will be available at `http://localhost:5000/`.

---

## Deploying to AWS Lambda with SAM

This project is configured for deployment to AWS Lambda using the AWS Serverless Application Model (SAM).

### Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with your credentials
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Docker (optional, but recommended for local builds)

### Project Structure

```
game-suggestion-api/
├── src/
├── lambda_handler.py
├── main.py
├── requirements.txt
├── template.yaml
└── ...
```

### Deployment Steps

1. **Build the application:**

   ```sh
   sam build
   ```

   This command will:

   - Install all dependencies from `requirements.txt` in a Lambda-compatible environment
   - Package your source code and dependencies for deployment

2. **Deploy the application:**

   ```sh
   sam deploy --guided
   ```

   - The `--guided` flag will prompt you for stack name, AWS region, and other deployment options.
   - After deployment, SAM will output the API Gateway endpoint URL.

3. **Set Environment Variables in Lambda:**

   - After deployment, go to the AWS Lambda Console.
   - Navigate to your function and add `OPENAI_KEY` and `STEAM_API_KEY` as environment variables.

   Alternatively, you can add these to the `Environment` section in `template.yaml` (not recommended for secrets in source control).

### API Gateway

- The deployed Lambda is fronted by an API Gateway.
- All HTTP methods and paths are proxied to your Flask app.

### Updating the Application

- Make code or dependency changes.
- Run `sam build` and `sam deploy` again.

---

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

---

## Testing

Tests are located in the `tests/` directory and use `pytest`.  
To run tests:

```sh
pytest
```

---

## Notes

- The database uses TinyDB and stores data in `db.json` by default.
- For development/testing, the database is mocked using pytest fixtures.
- Logging is enabled for debugging.

---

## License

MIT License
