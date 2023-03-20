from enum import Enum

from pydantic import BaseModel
from typing import Optional, Mapping, Union, MutableMapping


class SwarmObjectURL(str, Enum):
    SERVICE = 'services/{object_id}/logs'
    TASK = 'tasks/{object_id}/logs'


class ServiceCreate(BaseModel):
    name: Optional[str]
    labels: Optional[Mapping]
    task_template: Mapping
    mode: Optional[Mapping]
    update_config: Optional[Mapping]
    rollback_config: Optional[Mapping]
    networks: Optional[Mapping]
    endpoint_spec: Optional[Mapping]
    auth: Optional[Union[MutableMapping, str, bytes]]
    registry: Optional[str]
