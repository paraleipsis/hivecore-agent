from pydantic import BaseModel
from typing import Optional, Mapping


class ImageBuild(BaseModel):
    remote: Optional[str]
    fileobj: Optional[str]
    path_dockerfile: Optional[str]
    tag: Optional[str]
    quiet: Optional[bool]
    nocache: Optional[bool]
    buildargs: Optional[Mapping]
    pull: Optional[bool]
    rm: Optional[bool]
    forcerm: Optional[bool]
    labels: Optional[Mapping]
