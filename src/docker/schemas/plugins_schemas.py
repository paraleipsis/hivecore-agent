from pydantic import BaseModel
from typing import Optional, List


class PluginInstall(BaseModel):
    Name: Optional[str]
    Description: Optional[str]
    Value: Optional[List]
