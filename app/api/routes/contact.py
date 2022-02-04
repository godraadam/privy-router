from fastapi import APIRouter, HTTPException
from model.user import PrivyUser

from model.contact import PrivyContactCreate
import store
import requests
import json
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.post("/add")
def add_contact(payload: PrivyContactCreate):
    user:PrivyUser = store.get_current_user()
    daemon = user.private_daemon
    response = requests.post(f"http://127.0.0.1:{daemon.port}/api/contact/add", data=json.dumps(payload.dict()))
    return PlainTextResponse(status_code=response.status_code)