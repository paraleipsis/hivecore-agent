from typing import MutableMapping, List

from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200
from aiohttp import web

from modules.schemas import response_schemas as schemas
from report.schemas.schemas_docker_snapshot import DockerSnapshot
from utils.exceptions_utils import manage_exceptions
from report.services.service_docker_snapshot import get_docker_snapshot, get_docker_snapshot_on_event


class HostDockerSnapshotView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ) -> r200[schemas.GenericResponseModel[DockerSnapshot]]:
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            initial_snapshot = await get_docker_snapshot()
            await ws.send_json(initial_snapshot.dict())
            async for snapshot in get_docker_snapshot_on_event():
                if snapshot is None:
                    break
                await ws.send_json(snapshot.dict())
        finally:
            await ws.close()
            return ws
