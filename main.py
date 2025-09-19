import logging
from dotenv import load_dotenv
from uvicorn import run

logging.basicConfig(level=logging.INFO)
load_dotenv()

# import app after environment variables are loaded
from src import app

if __name__ == "__main__":
    run(app, port=5001)
