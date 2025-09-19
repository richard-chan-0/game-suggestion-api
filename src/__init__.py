from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.app.route import router

app = FastAPI()
app.include_router(router.player_router, prefix="/player")
app.include_router(router.commands_router, prefix="/commands")


@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )
