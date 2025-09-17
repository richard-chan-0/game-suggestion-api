from aws_lambda_wsgi import response
from src import app


def lambda_handler(event, context):
    # read s3 for db.json and write to /tmp/db.json

    return response(app, event, context)
