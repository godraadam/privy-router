
from pydantic import BaseModel


class PrivyMessage(BaseModel):
    recipient_alias: str # alias of recipient
    message: str # the message
