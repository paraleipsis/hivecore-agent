from pydantic import BaseModel
from typing import Optional, Mapping


class VolumeCreate(BaseModel):
    Name: str
    Driver: Optional[str]
    DriverOpts: Optional[Mapping]
    Labels: Optional[Mapping]
    ClusterVolumeSpec: Optional[Mapping]
