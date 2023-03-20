from pydantic import BaseModel
from typing import Optional, Mapping


class SwarmInit(BaseModel):
    Name: str
    Labels: Optional[Mapping]
    Data: str
    Templating: Optional[Mapping]


class SwarmJoin(BaseModel):
    Name: str
    Labels: Optional[Mapping]
    Data: str
    Templating: Optional[Mapping]


class SwarmUpdate(BaseModel):
    Name: str
    Labels: Optional[Mapping]
    Data: str
    Templating: Optional[Mapping]
