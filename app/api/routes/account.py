import logging
from typing import List
from pydantic import BaseModel

import requests

from fastapi import APIRouter, HTTPException
from app.model.user import PrivyUser, PrivyUserCreate, PrivyUserCredentials
from app.model.daemon import AddProxyPayload
from app.service import account_service
from app.config import settings
from app import store, util

router = APIRouter()

logger = logging.getLogger(__name__)


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


@router.post("/remove-locally")
def remove_account(credentials: PrivyUserCredentials):
    user = store.get_user_by_name(credentials.username)
    if user is None:
        raise HTTPException(status_code=404)
    if credentials.mnemonic != user.mnemonic:
        raise HTTPException(status_code=403)
    account_service.remove_account(user)
    store.reset_current_user()
    return user.username
    
@router.post("/remove-permanently")
def remove_account_permanent(credentials: PrivyUserCredentials):
    user = store.get_user_by_name(credentials.username)
    if user is None:
        raise HTTPException(status_code=404)
    if credentials.mnemonic != user.mnemonic:
        raise HTTPException(status_code=403)
    # ask the local node to nuke the database
    account_service.remove_account(user)
    store.reset_current_user()
    return user.username


@router.get("/ls", response_model=List[PrivyUser], response_model_include={"username"})
def list_local_accounts():
    return store.get_all_users()


@router.post("/add-proxy/{alias:str}")
def add_proxy_to_account(alias: str):
    user = store.get_current_user()
    if not user:
        raise HTTPException(status_code=403)
    daemon = user.private_daemon
    logger.info(f'Sending proxy request to {daemon.name}')
    return requests.post(f"{settings.APP_HOST}:{daemon.port}/api/contact/add-proxy/{alias}")



@router.post('/node/add-proxy/')
def add_proxy_node_side(payload: AddProxyPayload):
    logger.info(f'Received proxy response from {payload.to}')
    user = store.get_user_by_name(payload.to)
    if not user:
        raise HTTPException(status_code=404)
    account_service.add_proxy_to_account(payload)
