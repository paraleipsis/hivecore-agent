from typing import MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.client import daemon
from docker.schemas import system_schemas
from modules.schemas import response_schemas as schemas
from modules.utils.exceptions_utils import manage_exceptions


class SystemInfoView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            info = await daemon.get_system(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=info
                ).dict()
            )


class VersionView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            info = await daemon.get_version(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=info
                ).dict()
            )


class SystemDataUsageView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            info = await daemon.get_system_df(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=info
                ).dict()
            )


class SystemPruneView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            volumes: bool = False
    ) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await daemon.prune_system(
                docker_session=session,
                volumes=volumes
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class AuthView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            credentials: system_schemas.AuthCredentials
    ) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await daemon.docker_login(
                docker_session=session,
                credentials=credentials.dict()
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class SystemEventsView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                events_subscriber = daemon.docker_events_subscriber(
                    docker_session=session
                )
                while True:
                    message = await events_subscriber.get()
                    if message is None:
                        break
                    await ws.send_str(str(message))
        finally:
            await ws.close()


class PingView(PydanticView):
    @manage_exceptions
    async def get(
            self
    ) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            info = await daemon.ping(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=info
                ).dict()
            )
