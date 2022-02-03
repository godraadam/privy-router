from typing import List, Optional
from model.daemon import PrivyDaemon

from model.user import PrivyUser
from config import settings
import pickle

_users: List[PrivyUser] = []

_current_user: Optional[PrivyUser] = None


def read_from_disk():
    global _users
    """
    Read and parse users list (with their corresponding daemons)
    """
    try:
        with open(settings.STORE_PATH, "rb") as f:
            _users = pickle.load(file=f)
    except IOError:
        _users = []

def write_to_disk():
    """
    Persist users list (with their corresponding daemons)
    """
    with open(settings.STORE_PATH, "wb") as f:
        pickle.dump(obj=_users, file=f)


def save_user(user: PrivyUser) -> PrivyUser:
    _users.append(user)
    write_to_disk()
    return user
    
def remove_user(username: str) -> PrivyUser:
    global _users
    user = get_user_by_name(username)
    _users = list(filter(lambda user: user.username != username, _users))
    write_to_disk()
    return user


def get_user_by_id(id: str) -> Optional[PrivyUser]:
    result = list(filter(lambda user: user.id == id, _users))
    return result[0] if len(result) > 0 else None


def get_user_by_name(username: str) -> Optional[PrivyUser]:
    result = list(filter(lambda user: user.username == username, _users))
    return result[0] if len(result) > 0 else None


def get_all_users() -> List[PrivyUser]:
    return _users


def get_current_user() -> Optional[PrivyUser]:
    return _current_user

def set_current_user(user: PrivyUser):
    global _current_user
    _current_user = user
    
def reset_current_user():
    global _current_user
    _current_user = None

def save_daemon(daemon: PrivyDaemon, user: PrivyUser) -> PrivyDaemon:
    user.daemons.append(daemon)
    write_to_disk()
    return daemon
