from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.client import secrets
from swarm.schemas import secrets_schemas, schemas
from utils.exceptions_utils import manage_exceptions


class SecretCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            secrets_list = await secrets.list_secrets(
                docker_session=session,
                filters=filters
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=secrets_list,
                    total=len(secrets_list)
                ).dict()
            )


class SecretCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            secrets_details_list = await secrets.get_secrets(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=secrets_details_list,
                    total=len(secrets_details_list)
                ).dict()
            )


class SecretInspectView(PydanticView):
    @manage_exceptions
    async def get(self, secret_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            secret_details = await secrets.inspect_secret(
                docker_session=session,
                secret_id=secret_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=secret_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, secret_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await secrets.remove_secret(
                docker_session=session,
                secret_id=secret_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class SecretCreateView(PydanticView):
    @manage_exceptions
    async def post(self, config: secrets_schemas.SecretCreate) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await secrets.create_secret(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
