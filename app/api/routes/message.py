from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import requests

from app.model.message import PrivyMessage
from app import store
from app.config import settings

router = APIRouter()


@router.post("/send")
def send_message_to(msg_object: PrivyMessage):
    user = store.get_current_user()
    response = requests.post(
        f"{settings.APP_HOST}:{user.private_daemon.port}/api/message/send",
        json={"to": msg_object.recipient_alias, "msg": msg_object.message},
    )
    if response.status_code == 200:
        return PlainTextResponse(status_code=200, content="Message sent!")
    else:
        return PlainTextResponse(status_code=response.status_code)
        
@router.get("/all-incoming")
def get_all_messages():
    user = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    response = requests.get(f"{settings.APP_HOST}:{user.private_daemon.port}/api/message/all-incoming")
    return response.json()
    
@router.get("/all-outgoing")
def get_all_messages():
    user = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    response = requests.get(f"{settings.APP_HOST}:{user.private_daemon.port}/api/message/all-outgoing")
    return response.json()
    
@router.get("/with/{alias}")
def get_messages_with(alias: str):
    user = store.get_current_user()
    if not user:
        return PlainTextResponse(status_code=403)
    response = requests.get(f"{settings.APP_HOST}:{user.private_daemon.port}/api/message/with/{alias}")
    return response.json()
