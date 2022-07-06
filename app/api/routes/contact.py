from fastapi import APIRouter
from app.model.user import PrivyUser

from app.model.contact import PrivyContactCreate, PrivyContactUpdate
from app import store
import requests
from fastapi.responses import PlainTextResponse
from app.config import settings

router = APIRouter()


@router.post("/add")
def add_contact(payload: PrivyContactCreate):
    user: PrivyUser = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    daemon = user.private_daemon
    response = requests.post(
        f"{settings.APP_HOST}:{daemon.port}/api/contact/add", json=payload.dict()
    )
    return PlainTextResponse(status_code=response.status_code)


@router.delete("/rm/{alias}")
def remove_contact(alias: str):
    user: PrivyUser = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    daemon = user.private_daemon
    response = requests.delete(f"{settings.APP_HOST}:{daemon.port}/api/contact/rm/{alias}")
    return PlainTextResponse(status_code=response.status_code)


@router.get("/ls")
def get_contacts():
    user: PrivyUser = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    daemon = user.private_daemon
    response = requests.get(f"{settings.APP_HOST}:{daemon.port}/api/contact/ls")
    return response.json()


@router.get("/{alias}")
def get_contact_by_alias(alias: str):
    user: PrivyUser = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    daemon = user.private_daemon
    response = requests.get(f"{settings.APP_HOST}:{daemon.port}/api/contact/{alias}")
    return response.json()
    
@router.put("/{alias}")
def update_contact(alias: str, payload: PrivyContactUpdate):
    user: PrivyUser = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    daemon = user.private_daemon
    response = requests.put(f"{settings.APP_HOST}:{daemon.port}/api/contact/{alias}", json=payload.dict())
    return response
