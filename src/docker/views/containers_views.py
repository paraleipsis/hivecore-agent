import asyncio

from typing import Mapping, MutableMapping, List, Optional, Union

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.client import containers
from docker.schemas import containers_schemas
from docker.schemas import schemas
from utils.exceptions_utils import manage_exceptions


class ContainerCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, list_all: bool = False, size: bool = False,
                  filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            containers_list = await containers.list_containers(
                docker_session=session,
                list_all=list_all,
                size=size,
                filters=filters
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=containers_list,
                    total=len(containers_list)
                ).dict(),
            )


class ContainerCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            containers_details_list = await containers.get_containers(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=containers_details_list,
                    total=len(containers_details_list)
                ).dict()
            )


class ContainerInspectView(PydanticView):
    @manage_exceptions
    async def get(self, container_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            container_details = await containers.inspect_container(
                docker_session=session,
                container_id=container_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=container_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, container_id: str, /, v: bool = False, link: bool = False,
                     force: bool = False) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.remove_container(
                docker_session=session,
                container_id=container_id,
                v=v,
                link=link,
                force=force
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerRunView(PydanticView):
    @manage_exceptions
    async def post(self, config: containers_schemas.ContainerCreate, name: Optional[str] = None,
                   auth: Optional[Union[Mapping, str, bytes]] = None) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await containers.run_container(
                docker_session=session,
                config=config.dict(),
                auth=auth,
                name=name
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerPruneView(PydanticView):
    @manage_exceptions
    async def post(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await containers.prune_containers(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerStartView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.start_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerStopView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.stop_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerRestartView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.restart_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerPauseView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.pause_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerUnpauseView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.unpause_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerKillView(PydanticView):
    @manage_exceptions
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await containers.kill_container(
                docker_session=session,
                container_id=container_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ContainerLogsView(PydanticView):
    @manage_exceptions
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                logs_subscriber = containers.container_logs_subscriber(
                    docker_session=session,
                    container_id=container_id,
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
            return ws


class ContainerStatsView(PydanticView):
    @manage_exceptions
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                stats_subscriber = containers.container_stats_subscriber(
                    docker_session=session,
                    container_id=container_id,
                )
                while True:
                    message = await stats_subscriber.get()
                    if message is None:
                        break
                    await ws.send_str(str(message))
        finally:
            await ws.close()
            return ws


class ContainerTerminalView(PydanticView):
    @manage_exceptions
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                terminal_session = await containers.container_terminal(
                    docker_session=session,
                    container_id=container_id
                )
                async with terminal_session as terminal:
                    task1 = asyncio.create_task(containers.read_terminal(terminal_session=terminal, ws=ws))
                    task2 = asyncio.create_task(containers.write_terminal(terminal_session=terminal, ws=ws))
                    await asyncio.gather(task1, task2)
        finally:
            await ws.close()
            return ws


class ContainerAttachView(PydanticView):

    async def get(self):
        return
