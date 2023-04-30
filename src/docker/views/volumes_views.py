from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.client import volumes
from docker.schemas import volumes_schemas
from modules.schemas import response_schemas as schemas
from utils.exceptions_utils import manage_exceptions


class VolumeCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            volumes_list = await volumes.list_volumes(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=volumes_list,
                    total=len(volumes_list)
                ).dict()
            )


class VolumeCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            volumes_details_list = await volumes.get_volumes(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=volumes_details_list,
                    total=len(volumes_details_list)
                ).dict()
            )


class VolumeInspectView(PydanticView):
    @manage_exceptions
    async def get(self, volume_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            volume_details = await volumes.inspect_volume(
                docker_session=session,
                volume_id=volume_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=volume_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, volume_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await volumes.remove_volume(
                docker_session=session,
                volume_id=volume_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class VolumeCreateView(PydanticView):
    @manage_exceptions
    async def post(self, config: volumes_schemas.VolumeCreate) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await volumes.create_volume(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class VolumePruneView(PydanticView):
    @manage_exceptions
    async def post(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await volumes.prune_volumes(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
