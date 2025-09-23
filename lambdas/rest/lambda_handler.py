from logging import getLogger, INFO, basicConfig
from json import dumps
from events import event_processor
from src.database.aws_tiny_db_handler import AwsTinyDBHandler

basicConfig(level=INFO, force=True)

logger = getLogger()


def lambda_handler(event, context):
    logger.info("Received event: %s", event)
    db_handler = AwsTinyDBHandler()
    db_handler.download_db_from_s3()

    event_response = event_processor(event)

    logger.info("Event processed successfully, response: %s", event_response)
    db_handler.upload_db_to_s3()
    return {
        "statusCode": 200,
        "body": dumps(event_response),
        "headers": {
            "Content-Type": "application/json",
        },
    }
