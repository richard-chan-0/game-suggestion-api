from handler import *


def process_gets(event):
    path = event.get("path")
    if path == "/player":
        return get_player_by_name(event)

    elif path.startswith("/player/"):
        return get_player_by_id(event)


def process_posts(event):
    path = event.get("path")
    if path == "/player":
        return add_player(event)


def event_controller(event):
    """
    Process incoming events and route them to the appropriate handler.
    """
    method = event.get("httpMethod")

    if method == "GET":
        return process_gets(event)

    elif method == "POST":
        return process_posts(event)
