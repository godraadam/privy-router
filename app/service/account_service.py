import uuid
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
        username=payload.username, password=payload.password, daemons=[daemon], private_daemon=daemon
    )
    daemon_service.start_daemons_for_user(user)
    return store.save_user(user)


def remove_account(user: PrivyUser):
    daemon_service.remove_daemons_for_user(user)
    store.remove_user(user.username)