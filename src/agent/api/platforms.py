from typing import MutableMapping

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from modules.schemas import response_schemas as schemas
from modules.utils.exceptions_utils import manage_exceptions
from agent.services.service_platforms import (get_active_platforms)


class ActivePlatformsView(PydanticView):
    @manage_exceptions
    async def get(
            self,
    ) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        active_platforms = await get_active_platforms()
        return web.json_response(
            data=schemas.GenericResponseModel(
                data=active_platforms,
                total=len(active_platforms)
            ).dict(),
        )
