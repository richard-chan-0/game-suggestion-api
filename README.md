# Game Suggestion API

## Overview

A FastAPI-based API for suggesting multiplayer games based on Steam libraries, with OpenAI integration for game recommendations. The application is designed to be modular, scalable, and deployable to AWS Lambda using the AWS Serverless Application Model (SAM).

---

## Architecture

### **Technologies**

- **FastAPI**: For building the API.
- **AWS Lambda**: For serverless deployment.
- **API Gateway**: To expose the Lambda function as an HTTP endpoint.
- **TinyDB**: Lightweight NoSQL database for storing player and game data.
- **OpenAI API**: For generating game suggestions.
- **Steam API**: For fetching player game libraries.
- **Mangum**: ASGI adapter for running FastAPI on AWS Lambda.

### **Project Structure**

```
game-suggestion-api/
├── src/
│   ├── __init__.py
│   ├── lambda_handler.py         # Entry point for AWS Lambda
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database/             # Database layer
│   │   │   ├── constants.py
│   │   │   ├── entities.py
│   │   │   ├── entity_factory.py
│   │   │   ├── wrapper/          # Database wrappers
│   │   │       ├── database_wrapper.py
│   │   │       ├── game_wrapper.py
│   │   │       ├── player_wrapper.py
│   │   │       ├── ref_wrapper.py
│   │   ├── lib/                  # Utility functions and exceptions
│   │   │   ├── exceptions.py
│   │   │   ├── string_utils.py
│   │   ├── route/                # API routes
│   │       ├── router/
│   │           ├── commands.py
│   │           ├── game.py
│   │           ├── player.py
│   ├── service/
│       ├── apis/                 # External API integrations
│       │   ├── openai_api_wrapper.py
│       │   ├── steam_api_wrapper.py
│       ├── logic/                # Business logic
│           ├── commands.py
│           ├── game.py
│           ├── player.py
├── requirements.txt              # Python dependencies
├── README.md                     # Documentation
├── template.yaml                 # AWS SAM template for deployment
└── tests/                        # Unit tests
```

---

## Features

- **Player Management**:
  - Add and search for players by Steam ID or name.
  - Retrieve player details by ID.
- **Game Management**:
  - Refresh and store owned games for players from the Steam API.
  - Get shared games between players.
  - Get AI-powered game suggestions for a group.
- **Database**:
  - Modular database layer using TinyDB for lightweight storage.
- **Serverless Deployment**:
  - Deployable to AWS Lambda with API Gateway integration.

---

## Setup (Local Development)

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/game-suggestion-api.git
cd game-suggestion-api
```

### 2. Install Dependencies

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
export TINYDB_BUCKET="your_s3_bucket_name"
```

Alternatively, create a `.env` file in the project root:

```
OPENAI_KEY=your_openai_api_key
STEAM_API_KEY=your_steam_api_key
TINYDB_BUCKET=your_s3_bucket_name
```

### 4. Run the API Locally

Use Uvicorn to run the FastAPI application:

```sh
uvicorn src.__init__:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at `http://localhost:5000/`.

---

## Deployment to AWS Lambda

This project is configured for deployment to AWS Lambda using the AWS Serverless Application Model (SAM).

### Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with your credentials.
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
- Docker (optional, but recommended for local builds).

### Deployment Steps

1. **Build the Application**:

   ```sh
   sam build
   ```

   This command will:

   - Install all dependencies from `requirements.layer.txt` in a Lambda-compatible environment.
   - Package your source code and dependencies for deployment.
   - run this command: `pip install -r requirements.layer.txt -t layer/python/lib/python3.12/site-packages`

2. **Deploy the Application**:

   ```sh
   sam deploy --guided
   ```

   - The `--guided` flag will prompt you for stack name, AWS region, and other deployment options.
   - After deployment, SAM will output the API Gateway endpoint URL.

3. **Set Environment Variables in Lambda**:

   - After deployment, go to the AWS Lambda Console.
   - Navigate to your function and add `OPENAI_KEY`, `STEAM_API_KEY`, and `TINYDB_BUCKET` as environment variables.

   Alternatively, you can add these to the `Environment` section in `template.yaml` (not recommended for secrets in source control).

---

## Testing

### Running Unit Tests

Tests are located in the `tests/` directory and use `pytest`. To run tests:

```sh
pytest
```

### Testing the API Locally

Use tools like **Postman** or **cURL** to test the API endpoints. For example:

```sh
curl -X POST http://localhost:5000/player/ \
    -H "Content-Type: application/json" \
    -d '{"steam_id": "12345", "first_name": "John", "last_name": "Doe"}'
```

---

## API Endpoints

### Player Endpoints

- `POST /player/`  
  Add a player.  
  **JSON body:**

  ```json
  {
    "steam_id": "12345",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

- `GET /player/`  
  Search for a player by `first_name` and `last_name` (query params).  
  Example:

  ```
  /player/?first_name=John&last_name=Doe
  ```

- `GET /player/{id}`  
  Get player by internal database ID.

### Commands Endpoints

- `GET /refresh`  
  Refresh all players' owned games from Steam.

- `POST /shared`  
  Get shared games for a list of players.  
  **JSON body:**

  ```json
  {
    "steam_ids": ["12345", "67890"]
  }
  ```

- `POST /suggest`  
  Get an AI-powered game suggestion for a group.  
  **JSON body:**
  ```json
  {
    "steam_ids": ["12345", "67890"]
  }
  ```

---

## Notes

- The database uses TinyDB and stores data in `db.json` by default.
- For production, ensure sensitive data like API keys are stored securely (e.g., AWS Secrets Manager).
- Logging is enabled for debugging and can be configured in `src/lambda_handler.py`.

---

## License

MIT License
