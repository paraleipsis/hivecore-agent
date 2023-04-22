from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.client import services
from swarm.schemas import services_schemas, schemas
from utils.exceptions_utils import manage_exceptions


class ServiceCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None,
                  status: bool = False) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            services_list = await services.list_services(
                docker_session=session,
                filters=filters,
                status=status
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=services_list,
                    total=len(services_list)
                ).dict()
            )


class ServiceCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            services_details_list = await services.get_services(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=services_details_list,
                    total=len(services_details_list)
                ).dict()
            )


class ServiceInspectView(PydanticView):
    @manage_exceptions
    async def get(self, service_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            service_details = await services.inspect_service(
                docker_session=session,
                service_id=service_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=service_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, service_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await services.remove_service(
                docker_session=session,
                service_id=service_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ServiceCreateView(PydanticView):
    @manage_exceptions
    async def post(self, config: services_schemas.ServiceCreate) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await services.create_service(
                docker_session=session,
                config=config.dict(),
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ServiceLogsView(PydanticView):
    @manage_exceptions
    async def get(self, service_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        try:
            async with Docker() as session:
                logs_subscriber = services.service_logs_subscriber(
                    docker_session=session,
                    service_id=service_id,
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
