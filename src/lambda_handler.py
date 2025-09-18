from os import getenv
from boto3 import client
from awsgi import response
from src import app
from botocore.exceptions import ClientError
from src.app.lib.exceptions import AwsException
from logging import getLogger
from mangum import Mangum

logger = getLogger(__name__)
logger.setLevel("INFO")

TINYDB_BUCKET = getenv("TINYDB_BUCKET")

handler = Mangum(app)


def create_s3_client():
    return client("s3")


def download_db_from_s3(s3_client):
    key = "db.json"
    download_path = "/tmp/db.json"
    try:
        s3_client.download_file(TINYDB_BUCKET, key, download_path)
    except ClientError as e:
        raise AwsException(f"Error downloading DB from S3: {e}")


def upload_db_to_s3(s3_client):
    key = "db.json"
    upload_path = "/tmp/db.json"
    try:
        s3_client.upload_file(upload_path, TINYDB_BUCKET, key)
    except ClientError as e:
        raise AwsException(f"Error uploading DB to S3: {e}")


def lambda_handler(event, context):
    if not TINYDB_BUCKET:
        raise ValueError("TINYDB_BUCKET environment variable is not set")

    s3_client = create_s3_client()
    download_db_from_s3(s3_client)

    logger.info("Processing event: %s", event)
    event_response = handler(event, context)

    upload_db_to_s3(s3_client)

    logger.info("Event processed successfully, response: %s", event_response)
    return event_response
