from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.client import tasks
from modules.schemas import response_schemas as schemas
from modules.utils.exceptions_utils import manage_exceptions


class TaskCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            tasks_list = await tasks.list_tasks(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=tasks_list,
                    total=len(tasks_list)
                ).dict()
            )


class TaskCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            tasks_details_list = await tasks.get_tasks(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=tasks_details_list,
                    total=len(tasks_details_list)
                ).dict()
            )


class TaskInspectView(PydanticView):
    @manage_exceptions
    async def get(self, task_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            task_details = await tasks.inspect_task(
                docker_session=session,
                task_id=task_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=task_details,
                ).dict()
            )


class TaskLogsView(PydanticView):
    @manage_exceptions
    async def get(self, task_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                logs_subscriber = tasks.task_logs_subscriber(
                    docker_session=session,
                    task_id=task_id,
                    stdout=True,
                    stderr=True,
                    follow=True
                )
                while True:
                    message = await logs_subscriber.get()
                    if message is None:
                        break
                    await ws.send_str(str(message))
        finally:
            await ws.close()
