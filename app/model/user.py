from typing import List
import uuid
from pydantic import BaseModel

from app.model.daemon import PrivyDaemon


class PrivyUser(BaseModel):
    username: str  # should be unique
    password: str
    private_daemon: PrivyDaemon
    daemons: List[PrivyDaemon] = [] # list of daemons including proxies


class PrivyUserCreate(BaseModel):
    # TODO: maybe replace with token and seed?
    username: str
    password: str


class PrivyUserLogin(BaseModel):
    username: str
    password: str
