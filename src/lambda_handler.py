from aws_lambda_wsgi import response
from src.app import app


def lambda_handler(event, context):
    return response(app, event, context)
