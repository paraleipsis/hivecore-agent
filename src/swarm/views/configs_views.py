from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.client import configs
from swarm.schemas import configs_schemas
from modules.schemas import response_schemas as schemas
from utils.exceptions_utils import manage_exceptions


class ConfigCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            configs_list = await configs.list_configs(
                docker_session=session,
                filters=filters
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=configs_list,
                    total=len(configs_list)
                ).dict()
            )


class ConfigCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            configs_details_list = await configs.get_configs(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=configs_details_list,
                    total=len(configs_details_list)
                ).dict()
            )


class ConfigInspectView(PydanticView):
    @manage_exceptions
    async def get(self, config_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            config_details = await configs.inspect_config(
                docker_session=session,
                config_id=config_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=config_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, config_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await configs.remove_config(
                docker_session=session,
                config_id=config_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ConfigCreateView(PydanticView):
    @manage_exceptions
    async def post(self, config: configs_schemas.ConfigCreate) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await configs.create_config(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
