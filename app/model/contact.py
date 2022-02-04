from pydantic import BaseModel

class PrivyContactCreate(BaseModel):
    alias: str
    pubkey: str
    trusted: bool = False
    
class PrivyContact(PrivyContactCreate):
    address: str