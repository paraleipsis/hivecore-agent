from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List, Any, Dict, Mapping
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class GenericResponseModel(GenericModel, Generic[DataT]):
    success: bool = Field(True)
    error_msg: Optional[str] = Field(None, alias='errorMsg')
    data: Optional[DataT] = Field(None)
    total: Optional[int] = Field(None)

    class Config:
        allow_population_by_field_name = True


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
    Env: Optional[List[str]]
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

