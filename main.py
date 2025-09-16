from dotenv import load_dotenv
from src.app import app

import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
