from typing import Optional
import uuid

from app.model.daemon import PrivyDaemon
from app.model.user import PrivyUser, PrivyUserCreate
from app.service import daemon_service
from app import store


def add_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "remote")


def create_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "origin")


def add_or_create_account(payload: PrivyUserCreate, type: str) -> PrivyUser:
    daemon_name = f"{payload.username}-{type}"
    
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type=type,
        name=daemon_name,
        repo=uuid.uuid4().hex,
    )
    user = PrivyUser(
        username=payload.username,
        password=payload.password,
        daemons=[daemon],
        private_daemon=daemon,
    )
    daemon_service.start_daemon(daemon=daemon, user=user)
    return store.save_user(user)


def remove_account(user: PrivyUser):
    daemon_service.remove_daemons_for_user(user)
    store.remove_user(user.username)


def add_proxy_to_account(user_name: str, proxy_pubkey: str):
    user: Optional[PrivyUser] = store.get_user_by_name(username=user_name)
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
