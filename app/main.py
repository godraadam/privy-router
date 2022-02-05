from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
from api import index
from service.daemon_service import start_daemons_for_user
from store import get_all_users, read_from_disk
from config import settings
import store

app = FastAPI()

app.include_router(index.router, prefix="/api")


def init():
    # read data
    read_from_disk()
    # for each user start daemon
    users = get_all_users()
    for user in users:
        start_daemons_for_user(user)


@app.on_event("startup")
def on_startup():
    init()


@app.middleware("http")
async def check_login(req: Request, call_next):
    if req.url.path not in [
        "/api/auth/login",
        "/api/auth/logout",
        "/api/auth/whoami",
        # TODO: these endpoints should require user to be logged out. Also, check as substr for account/remove, not exact match
        "/api/account/add",
        "/api/account/remove",
        "/api/account/create",
    ]:
        if store.get_current_user() is None:
            return PlainTextResponse(status_code=403)
    response = await call_next(req)
    return response


@app.get("/")
async def root():
    return {"message": "Privy Router is running"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)