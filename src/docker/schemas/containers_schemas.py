from pydantic import BaseModel
from typing import Optional, List, Mapping, Literal, Any


class ContainerVolumeBind(BaseModel):
    host_path: str
    container_path: str
    mode: Optional[Literal["ro", "rw"]] = "rw"


class ContainerPortsBind(BaseModel):
    host_port: str | List[str]
    container_port: str
    tcp: Optional[bool] = True
    udp: Optional[bool] = False


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
    PortsBind: Optional[List[ContainerPortsBind]]
    VolumesBind: Optional[List[ContainerVolumeBind]]

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Override the default dict method to exclude None values in the response."""

        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)
