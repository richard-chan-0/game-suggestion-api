from player import (
    ready_player,
    search_player,
    search_player_by_id,
)


def process_gets(event):
    path = event.get("path")
    query_params = event.get("queryStringParameters", {})
    path_params = event.get("pathParameters", {})

    if path == "/player":
        first_name = query_params.get("first_name")
        last_name = query_params.get("last_name")
        if not first_name or not last_name:
            raise ValueError("first_name and last_name query parameters are required")
        return search_player(first_name, last_name)

    elif path.startswith("/player/"):
        player_id = path_params.get("id")
        if not player_id:
            raise ValueError("Player ID is required")
        return search_player_by_id(player_id)


def process_posts(event):
    path = event.get("path")
    body = event.get("body", {})
    if path == "/player":
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        steam_id = body.get("steam_id")
        if not first_name or not last_name or not steam_id:
            raise ValueError(
                "first_name, last_name, and steam_id are required in the request body"
            )
        return ready_player(steam_id, first_name, last_name)


def event_processor(event):
    """
    Process incoming events and route them to the appropriate handler.
    """
    method = event.get("httpMethod")

    if method == "GET":
        return process_gets(event)

    elif method == "POST":
        return process_posts(event)
