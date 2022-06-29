from typing import List
import uuid
from pydantic import BaseModel

from app.model.daemon import PrivyDaemon


class PrivyUser(BaseModel):
    username: str  # should be unique
    mnemonic: str
    private_daemon: PrivyDaemon
    daemons: List[PrivyDaemon] = [] # list of daemons including proxies


class PrivyUserCredentials(BaseModel):
    username: str
    mnemonic: str
    
class PrivyUserCreate(BaseModel):
    username: str

