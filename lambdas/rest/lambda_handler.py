from logging import getLogger, INFO, basicConfig
from json import dumps

from src.app.lib.aws_tiny_db_handler import AwsTinyDBHandler

from src.app.service.logic.player import (
    ready_player,
    search_player,
    search_player_by_id,
)

basicConfig(level=INFO, force=True)

logger = getLogger()


def event_processor(event, context):
    method = event.get("httpMethod")
    path = event.get("path")
    query_params = event.get("queryStringParameters", {})
    path_params = event.get("pathParameters", {})

    if method == "GET" and path == "/player":
        first_name = query_params.get("first_name")
        last_name = query_params.get("last_name")
        if not first_name or not last_name:
            raise ValueError("first_name and last_name query parameters are required")
        return search_player(first_name, last_name)

    elif method == "GET" and path.startswith("/player/"):
        player_id = path_params.get("id")
        if not player_id:
            raise ValueError("Player ID is required")
        return search_player_by_id(player_id)

    elif method == "POST" and path == "/player":
        body = event.get("body")
        if not body:
            raise ValueError("Request body is required")

        first_name = body.get("first_name")
        last_name = body.get("last_name")
        steam_id = body.get("steam_id")
        return ready_player(first_name, last_name, steam_id)


def lambda_handler(event, context):
    logger.info("Received event: %s", event)
    db_handler = AwsTinyDBHandler()
    db_handler.download_db_from_s3()

    event_response = event_processor(event, context)

    logger.info("Event processed successfully, response: %s", event_response)
    db_handler.upload_db_to_s3()
    return {
        "statusCode": 200,
        "body": dumps(event_response),
        "headers": {
            "Content-Type": "application/json",
        },
    }
