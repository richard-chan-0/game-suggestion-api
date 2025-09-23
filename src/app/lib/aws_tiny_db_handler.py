from boto3 import client
from botocore.exceptions import ClientError
from src.app.lib.exceptions import AwsException
from os import getenv
from logging import getLogger

logger = getLogger(__name__)

TINYDB_BUCKET = getenv("TINYDB_BUCKET")


class AwsTinyDBHandler:

    def __init__(self):
        if not TINYDB_BUCKET:
            raise ValueError("TINYDB_BUCKET environment variable is not set")
        self.client = client("s3")
        self.lambda_db_path = "/tmp/db.json"
        self.db_key = "db.json"

    def download_db_from_s3(self):
        try:
            logger.info("Downloading DB from S3...")
            self.client.download_file(TINYDB_BUCKET, self.db_key, self.lambda_db_path)
        except ClientError as e:
            raise AwsException(f"Error downloading DB from S3: {e}")

    def upload_db_to_s3(self):
        try:
            logger.info("Uploading DB to S3...")
            self.client.upload_file(self.lambda_db_path, TINYDB_BUCKET, self.db_key)
        except ClientError as e:
            raise AwsException(f"Error uploading DB to S3: {e}")
