from typing import Optional, Mapping, Any

from pydantic.main import BaseModel


class ImageCreate(BaseModel):
    remote: Optional[str]
    fileobj: Optional[str]
    tag: Optional[str]
    nocache: Optional[bool] = False
    pull: Optional[bool] = False
    rm: Optional[bool] = True
    forcerm: Optional[bool] = False
    labels: Optional[Mapping]

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """Override the default dict method to exclude None values in the response."""

        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)
