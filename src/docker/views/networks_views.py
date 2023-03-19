from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.docker_api import networks
from docker.schemas import schemas, networks_schemas
from docker.utils import manage_exceptions


class NetworkCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            networks_list = await networks.list_networks(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=networks_list,
                    total=len(networks_list)
                ).dict()
            )


class NetworkCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            networks_details_list = await networks.get_networks(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=networks_details_list,
                    total=len(networks_details_list)
                ).dict()
            )


class NetworkInspectView(PydanticView):
    @manage_exceptions
    async def get(self, network_id: str, /, verbose: bool = False,
                  scope: str = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            network_details = await networks.inspect_network(
                docker_session=session,
                network_id=network_id,
                verbose=verbose,
                scope=scope
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=network_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, network_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await networks.remove_network(
                docker_session=session,
                network_id=network_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class NetworkCreateView(PydanticView):
    @manage_exceptions
    async def post(self, config: networks_schemas.NetworkCreate) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await networks.create_network(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class NetworkPruneView(PydanticView):
    @manage_exceptions
    async def post(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await networks.prune_networks(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class NetworkConnectContainerView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            network_id: str, /,
            config: networks_schemas.NetworkConnectContainer
    ) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await networks.connect_container_to_network(
                docker_session=session,
                network_id=network_id,
                config=config.dict()
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class NetworkDisconnectContainerView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            network_id: str, /,
            config: networks_schemas.NetworkDisconnectContainer
    ) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await networks.disconnect_container_from_network(
                docker_session=session,
                network_id=network_id,
                config=config.dict()
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
