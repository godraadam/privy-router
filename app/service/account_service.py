from typing import Optional
import uuid

from app.model.daemon import PrivyDaemon
from app.model.user import PrivyUser, PrivyUserCredentials
from app.model.daemon import AddProxyPayload
from app.service import daemon_service
from app import store, util

def add_account(payload: PrivyUserCredentials) -> PrivyUser:
    return add_or_create_account(payload, "remote")


def create_account(payload: PrivyUserCredentials) -> PrivyUser:
    return add_or_create_account(payload, "origin")

def add_or_create_account(payload: PrivyUserCredentials, type: str) -> PrivyUser:
    daemon_name = f"{payload.username}-{type}"
    
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type=type,
        name=daemon_name,
        repo=f'./orbitdb/{uuid.uuid4().hex}',
        port=util.get_available_port(6131)
    )
    user = PrivyUser(
        username=payload.username,
        mnemonic=payload.mnemonic,
        daemons=[daemon],
        private_daemon=daemon,
    )
    daemon_service.start_daemon(daemon=daemon, user=user)
    return store.save_user(user)


def remove_account(user: PrivyUser):
    store.remove_user(user.username)


def add_proxy_to_account(payload: AddProxyPayload):
    user: Optional[PrivyUser] = store.get_user_by_name(username=payload.to)
    if user is None:
        return
    proxy_daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type="proxy",
        name=f"{user.username}-proxy-{payload.proxy_pubkey[0:8]}",
        proxy_pubkey=payload.proxy_pubkey,
        token=payload.token,
        repo=f'./orbitdb/{uuid.uuid4().hex}',
        port=util.get_available_port()
    )
    user.daemons.append(proxy_daemon)
    daemon_service.start_daemon(proxy_daemon, user)
    store.write_to_disk()
