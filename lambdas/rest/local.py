"""fast api handler for local lambda function testing"""

from fastapi import FastAPI, Request, HTTPException
from player import ready_player, search_player, search_player_by_id
from uvicorn import run
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/player")
async def get_player(first_name: str, last_name: str):
    if not first_name or not last_name:
        raise HTTPException(
            status_code=400, detail="first_name and last_name are required"
        )
    return search_player(first_name, last_name)


@app.get("/player/{id}")
async def get_player_by_id(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="Player ID is required")
    return search_player_by_id(id)


@app.post("/player")
async def add_player(request: Request):
    body = await request.json()
    first_name = body.get("first_name")
    last_name = body.get("last_name")
    steam_id = body.get("steam_id")
    if not first_name or not last_name or not steam_id:
        raise HTTPException(
            status_code=400, detail="first_name, last_name, and steam_id are required"
        )
    return ready_player(steam_id, first_name, last_name)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
