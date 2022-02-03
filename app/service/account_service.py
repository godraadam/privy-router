import uuid
from model.daemon import PrivyDaemon
from model.user import PrivyUser, PrivyUserCreate
from . import daemon_service
import store


def add_account(payload: PrivyUserCreate) -> PrivyUser:
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type="remote",
        name=f"{payload.username}-remote",
        repo=uuid.uuid4().hex,
    )
    user = PrivyUser(
        username=payload.username, password=payload.password, daemons=[daemon]
    )
    daemon_service.start_daemons_for_user(user)
    return store.save_user(user)
    
def create_account(payload: PrivyUserCreate) -> PrivyUser:
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type="origin",
        name=f"{payload.username}-remote",
        repo=uuid.uuid4().hex,
    )
    user = PrivyUser(
        username=payload.username, password=payload.password, daemons=[daemon]
    )
    daemon_service.start_daemons_for_user(user)
    return store.save_user(user)


def remove_account(user: PrivyUser):
    daemon_service.remove_daemons_for_user(user)
    store.remove_user(user)
