from os import getenv
from boto3 import client
from aws_lambda_wsgi import response
from src import app

TINYDB_BUCKET = getenv("TINYDB_BUCKET")


def create_s3_client():
    return client("s3")


def download_db_from_s3(s3_client):
    key = "db.json"
    download_path = "/tmp/db.json"
    s3_client.download_file(TINYDB_BUCKET, key, download_path)


def upload_db_to_s3(s3_client):
    key = "db.json"
    upload_path = "/tmp/db.json"
    s3_client.upload_file(upload_path, TINYDB_BUCKET, key)


def lambda_handler(event, context):
    if not TINYDB_BUCKET:
        raise ValueError("TINYDB_BUCKET environment variable is not set")

    s3_client = create_s3_client()
    download_db_from_s3(s3_client)

    event_response = response(app, event, context)

    upload_db_to_s3(s3_client)
    return event_response
