from pydantic import BaseModel
from typing import Optional


class AuthCredentials(BaseModel):
    username: str
    password: Optional[str]
    email: Optional[str]
    serveraddress: Optional[str]
