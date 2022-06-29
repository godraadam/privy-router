from fastapi import APIRouter, HTTPException
import requests
from app.model.user import PrivyUserCredentials
from app import store
from app.config import settings


router = APIRouter()


@router.post("/login")
async def login(payload: PrivyUserCredentials):
    # set current user to this
    current_user = store.get_current_user()
    if current_user is not None:
        raise HTTPException(status_code=409)
    if len(store.get_all_users()) < 1:
        raise HTTPException(status_code=404)
    user = store.get_user_by_name(payload.username)
    if user is None:
        raise HTTPException(status_code=404)
    # check credentials
    if payload.mnemonic != user.mnemonic:
        raise HTTPException(status_code=401)
    store.set_current_user(user)
    return f"Logged in as {user.username}"


@router.post("/logout")
async def logout():
    store.reset_current_user()
    return f"Successfully logged out!"


@router.get("/whoami")
async def whoami():
    """
    Get display name of currently logged in user
    """
    current_user = store.get_current_user()
    if current_user is None:
        raise HTTPException(status_code=404, detail=f"Not logged in!")
    response = requests.get(f"{settings.APP_HOST}:{current_user.private_daemon.port}/api/account")
    pubkey = response.json()["pubkey"]
    return {"username": current_user.username, "pubkey": pubkey}
