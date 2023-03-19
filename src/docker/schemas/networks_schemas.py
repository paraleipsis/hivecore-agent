from pydantic import BaseModel
from typing import Optional, Mapping


class NetworkCreate(BaseModel):
    Name: str
    CheckDuplicate: Optional[bool]
    Driver: Optional[str]
    Internal: Optional[bool]
    Attachable: Optional[bool]
    nocache: Optional[bool]
    Ingress: Optional[bool]
    IPAM: Optional[Mapping]
    EnableIPv6: Optional[bool]
    Options: Optional[Mapping]
    Labels: Optional[Mapping]


class NetworkConnectContainer(BaseModel):
    Container: str
    EndpointConfig: Optional[Mapping]


class NetworkDisconnectContainer(BaseModel):
    Container: str
    Force: Optional[bool]
