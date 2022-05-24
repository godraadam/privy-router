from fastapi import APIRouter
from model.user import PrivyUser

from model.contact import PrivyContactCreate
import store
import requests
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.post("/add")
def add_contact(payload: PrivyContactCreate):
    user: PrivyUser = store.get_current_user()
    daemon = user.private_daemon
    response = requests.post(
        f"http://127.0.0.1:{daemon.port}/api/contact/add", json=payload.dict()
    )
    return PlainTextResponse(status_code=response.status_code)


@router.delete("/rm/{alias}")
def remove_contact(alias: str):
    user: PrivyUser = store.get_current_user()
    daemon = user.private_daemon
    response = requests.delete(f"http://127.0.0.1:{daemon.port}/api/contact/rm/{alias}")
    return PlainTextResponse(status_code=response.status_code)


@router.get("/ls")
def get_contacts():
    user: PrivyUser = store.get_current_user()
    daemon = user.private_daemon
    response = requests.get(f"http://127.0.0.1:{daemon.port}/api/contact/ls")
    return response.json()


@router.get("/{alias}")
def get_contact_by_alias(alias: str):
    user: PrivyUser = store.get_current_user()
    daemon = user.private_daemon
    response = requests.get(f"http://127.0.0.1:{daemon.port}/api/contact/{alias}")
    return response.json()
