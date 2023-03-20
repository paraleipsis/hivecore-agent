from pydantic import BaseModel
from typing import Optional, Mapping, Literal


class NodeSpec(BaseModel):
    Name: Optional[str]
    Labels: Optional[Mapping]
    Role: Literal['worker', 'manager']
    Availability: Literal['active', 'pause', 'drain']
