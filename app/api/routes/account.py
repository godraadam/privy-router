from typing import List

from fastapi import APIRouter, HTTPException
from app.model.user import PrivyUser, PrivyUserCreate, PrivyUserCredentials
from app.service import account_service
from app import store, util

router = APIRouter()


@router.post(
    "/add",
    response_model=PrivyUser,
    response_model_exclude={"password"},
    response_model_exclude_none=True,
)
def add_account(payload: PrivyUserCredentials):
    # check if username available locally
    if store.get_user_by_name(payload.username):
        raise HTTPException(status_code=409)
    return account_service.add_account(payload)

@router.post(
    "/create",
)
def register(payload: PrivyUserCreate):
    # check if username available locally
    if store.get_user_by_name(payload.username):
        raise HTTPException(status_code=409)
    words = util.get_mnemonic()
    credentials = PrivyUserCredentials(username=payload.username, mnemonic=words)
    account_service.create_account(credentials)
    return {"mnemonic": words}


@router.delete("/remove/{username:str}")
def remove_account(username: str):
    user = store.get_user_by_name(username)
    if user is None:
        raise HTTPException(status_code=404)
    account_service.remove_account(user)
    return user.username


@router.get("/ls", response_model=List[PrivyUser], response_model_include={"username"})
def list_local_accounts():
    return store.get_all_users()


@router.post("/{username:str}/add-proxy/{proxy_pubkey:str}")
def add_proxy_to_account(user_name: str, proxy_pubkey: str):
    return account_service.add_proxy_to_account(
        user_name=user_name, proxy_pubkey=proxy_pubkey
    )
