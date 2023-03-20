from pydantic import BaseModel
from typing import Optional, Mapping


class SecretCreate(BaseModel):
    Name: str
    Labels: Optional[Mapping]
    Data: str
    Driver: Optional[Mapping]
    Templating: Optional[Mapping]
