from fastapi import FastAPI
import uvicorn
from api import index
from service.daemon_service import start_daemons_for_user
from store import get_all_users, read_from_disk
from config import settings

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

@app.get("/")
async def root():
    return {"message":"Privy Router is running"}
    
if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)