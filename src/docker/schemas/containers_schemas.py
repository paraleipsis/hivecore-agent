from pydantic import BaseModel
from typing import Optional, List, Mapping


class ContainerCreate(BaseModel):
    Image: str
    Hostname: Optional[str]
    Domainname: Optional[str]
    User: Optional[str]
    AttachStdin: Optional[bool]
    AttachStdout: Optional[bool]
    AttachStderr: Optional[bool]
    Tty: Optional[bool]
    OpenStdin: Optional[bool]
    StdinOnce: Optional[bool]
    Env: Optional[Mapping]
    Cmd: Optional[List[str]]
    Entrypoint: Optional[str]
    Labels: Optional[Mapping]
    Volumes: Optional[Mapping]
    WorkingDir: Optional[str]
    NetworkDisabled: Optional[bool]
    MacAddress: Optional[str]
    ExposedPorts: Optional[Mapping]
    StopSignal: Optional[str]
    StopTimeout: Optional[int]
    HostConfig: Optional[Mapping]
    NetworkingConfig: Optional[Mapping]
