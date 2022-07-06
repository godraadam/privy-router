from typing import Optional
from pydantic import BaseModel


class PrivyDaemon(BaseModel):
    id: str
    type: str
    name: str
    repo: str
    proxy_pubkey: Optional[str]
    token: Optional[str]
    port: Optional[int]

class AddProxyPayload(BaseModel):
    to: str
    proxy_pubkey: str
    token: str
