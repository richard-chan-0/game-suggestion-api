def process_gets(event):
    path = event.get("path")
    query_params = event.get("queryStringParameters", {})
    path_params = event.get("pathParameters", {})

    return {}


def process_posts(event):
    path = event.get("path")
    body = event.get("body", {})
    return {}


def event_processor(event):
    """
    Process incoming events and route them to the appropriate handler.
    """
    method = event.get("httpMethod")

    if method == "GET":
        return process_gets(event)

    elif method == "POST":
        return process_posts(event)
