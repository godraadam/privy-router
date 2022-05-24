from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import uvicorn
from app.api import index
from app.service.daemon_service import start_daemons_for_user
from app.store import get_all_users, read_from_disk, get_current_user
from app.config import settings

app = FastAPI()

app.include_router(index.router, prefix="/api")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        "/api/ping",
        "/api/auth/login",
        "/api/auth/logout",
        "/api/auth/whoami",
        "/api/account/ls",
        # TODO: these endpoints should require user to be logged out. Also, check as substr for account/remove, not exact match
        "/api/account/add",
        "/api/account/remove",
        "/api/account/create",
    ]:
        if get_current_user() is None:
            return PlainTextResponse(status_code=403)
    response = await call_next(req)
    return response


@app.get("/")
async def root():
    return {"message": "Privy Router is running"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
