# Game Suggestion API

## Overview

This project uses an AWS Lambda-first architecture, leveraging AWS API Gateway for RESTful endpoints and Lambda functions for serverless execution. While FastAPI is still used for local development and testing, the primary deployment strategy has shifted to AWS-native services.

---

## Architecture

### **Technologies**

- **AWS Lambda**: Core compute layer for serverless execution.
- **API Gateway**: Exposes RESTful endpoints for the Lambda functions.
- **FastAPI**: Used for local development and testing.
- **TinyDB**: Lightweight NoSQL database for local data storage.
- **OpenAI API**: Provides AI-powered game recommendations.
- **Steam API**: Fetches player game libraries.
- **Shared Layers**: Common dependencies and shared code are packaged as Lambda layers.

### **Lambda Handlers**

1. **REST Endpoints**:

   - Located in `lambdas/rest/lambda_handler.py`.
   - Handles RESTful API requests for player and game management.

2. **RPC-like Endpoints**:
   - Located in `lambdas/commands/lambda_handler.py`.
   - Handles command-based operations like refreshing game data or executing batch tasks.

---

## Technical Considerations

### **Shared Dependencies and Code**

- Shared logic and dependencies are packaged as Lambda layers to reduce duplication and improve maintainability.
- Use the `copy_src_to_layer.sh` script to copy the `src` folder into the `shared-logic-layer/python` directory.

### **Environment Variables**

- Environment variables like `OPENAI_KEY`, `STEAM_API_KEY`, and `TINYDB_BUCKET` are configured in the Lambda function settings.

### **Local Development**

- FastAPI is used for local development to simulate API behavior.
- Run the FastAPI app locally using Uvicorn:
  ```sh
  uvicorn src.__init__:app --reload --host 0.0.0.0 --port 5000
  ```

---

## Deployment to AWS Lambda

### Prerequisites

- AWS CLI and SAM CLI installed and configured.
- Docker installed for building dependencies.

### Deployment Steps

1. **Prepare the Shared Layer**:

   ```sh
   ./copy_src_to_layer.sh
   ```

2. **Build the Application**:

   ```sh
   sam build
   ```

3. **Deploy the Application**:
   ```sh
   sam deploy --guided --config-file [dev,prod]
   ```

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
