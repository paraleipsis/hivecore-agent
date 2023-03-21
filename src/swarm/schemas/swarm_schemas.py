from pydantic import BaseModel
from typing import Optional, Mapping, List


class SwarmInit(BaseModel):
    ListenAddr: str = '0.0.0.0:2377'
    AdvertiseAddr: Optional[str]
    DataPathAddr: Optional[str]
    DataPathPort: Optional[int]
    DefaultAddrPool: Optional[List[str]]
    ForceNewCluster: Optional[bool]
    SubnetSize: Optional[int]
    Spec: Optional[Mapping]


class SwarmJoin(BaseModel):
    ListenAddr: str = '0.0.0.0:2377'
    AdvertiseAddr: Optional[str]
    DataPathAddr: Optional[str]
    RemoteAddrs: List[str]
    JoinToken: str


class SwarmUpdate(BaseModel):
    Name: Optional[str]
    Labels: Optional[Mapping]
    Orchestration: Optional[Mapping]
    Raft: Optional[Mapping]
    Dispatcher: Optional[Mapping]
    CAConfig: Optional[Mapping]
    EncryptionConfig: Optional[Mapping]
    TaskDefaults: Optional[Mapping]
