import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

# import app after environment variables are loaded
from src import app


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
