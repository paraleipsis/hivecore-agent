from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.docker_api import plugins
from docker.schemas import schemas, plugins_schemas
from docker.utils import manage_exceptions


class PluginCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            plugins_list = await plugins.list_plugins(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=plugins_list,
                    total=len(plugins_list)
                ).dict()
            )


class PluginCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            plugins_details_list = await plugins.get_plugins(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=plugins_details_list,
                    total=len(plugins_details_list)
                ).dict()
            )


class PluginInspectView(PydanticView):
    @manage_exceptions
    async def get(self, plugin_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            plugin_details = await plugins.inspect_plugin(
                docker_session=session,
                plugin_id=plugin_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=plugin_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, plugin_id: str, /, force: bool = False) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await plugins.remove_plugin(
                docker_session=session,
                plugin_id=plugin_id,
                force=force
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class PluginInstallView(PydanticView):
    @manage_exceptions
    async def post(self, config: plugins_schemas.PluginInstall,
                   remote: str, name: str = None) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await plugins.install_plugin(
                docker_session=session,
                remote=remote,
                name=name,
                config=config.dict()
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class PluginEnableView(PydanticView):
    @manage_exceptions
    async def post(self, plugin_id: str, /, timeout: int = 0) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await plugins.enable_plugin(
                docker_session=session,
                plugin_id=plugin_id,
                timeout=timeout
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class PluginDisableView(PydanticView):
    @manage_exceptions
    async def post(self, plugin_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await plugins.disable_plugin(
                docker_session=session,
                plugin_id=plugin_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
