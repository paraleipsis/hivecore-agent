from pydantic import BaseModel
from typing import Optional, Mapping


class ConfigCreate(BaseModel):
    Name: str
    Labels: Optional[Mapping]
    Data: str
    Templating: Optional[Mapping]
