from typing import Optional
import uuid

from requests import request
import requests
from model.daemon import PrivyDaemon
from model.user import PrivyUser, PrivyUserCreate
from . import daemon_service
import store


def add_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "remote")


def create_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "origin")


def add_or_create_account(payload: PrivyUserCreate, type: str) -> PrivyUser:
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type=type,
        name=f"{payload.username}-{type}",
        repo=uuid.uuid4().hex,
    )
    user = PrivyUser(
        username=payload.username,
        password=payload.password,
        daemons=[daemon],
        private_daemon=daemon,
    )
    daemon_service.start_daemons_for_user(user)
    res = requests.get(f"http://127.0.0.1:{daemon.port}/account/")
    if res.status_code == 200:
        user_address = dict(res.json())["address"]
        user.address = user_address
    else:
        print("Failed to fetch user address...")
    return store.save_user(user)


def remove_account(user: PrivyUser):
    daemon_service.remove_daemons_for_user(user)
    store.remove_user(user.username)


def add_proxy_to_account(user_address: str, proxy_pubkey: str):
    user: Optional[PrivyUser] = store.get_user_by_address(address=user_address)
    if user is None:
        return
    proxy_daemon = PrivyDaemon(
        type="proxy",
        name=f"{user.username}-proxy-{proxy_pubkey[0:8]}",
        proxy_pubkey=proxy_pubkey,
        repo=uuid.uuid4().hex,
    )
    user.daemons.append(proxy_daemon)
    daemon_service.start_daemon(proxy_daemon)
    return store.save_user(user)
