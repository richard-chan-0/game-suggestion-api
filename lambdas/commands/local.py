"""fast api handler for local lambda function testing"""

from fastapi import FastAPI, Request, HTTPException
from handler import (
    refresh_shared_games,
    get_shared_games_for_all_players,
    suggest_games_for_all_players,
    get_shared_games_for_steam_ids,
    suggest_games,
)
from uvicorn import run
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/refresh")
async def refresh():
    return refresh_shared_games()


@app.get("/shared")
async def get_shared():
    return get_shared_games_for_all_players()


@app.post("/shared")
async def get_shared_for_steam_ids(request: Request):
    body = await request.json()
    steam_ids = body.get("steam_ids", [])
    if not steam_ids:
        raise HTTPException(
            status_code=400, detail="Missing 'steam_ids' in request body"
        )
    return get_shared_games_for_steam_ids(steam_ids)


@app.get("/suggest")
async def suggest():
    return suggest_games_for_all_players()


@app.post("/suggest")
async def suggest_for_steam_ids(request: Request):
    body = await request.json()
    steam_ids = body.get("steam_ids", [])
    if not steam_ids:
        raise HTTPException(
            status_code=400, detail="Missing 'steam_ids' in request body"
        )
    return suggest_games(steam_ids)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
