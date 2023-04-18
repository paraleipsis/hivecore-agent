from typing import Mapping, MutableMapping

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.swarm_api import swarm
from swarm.schemas import swarm_schemas, schemas
from swarm.utils import manage_exceptions


class SwarmInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            swarm_details = await swarm.inspect_swarm(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=swarm_details,
                ).dict()
            )


class SwarmInitView(PydanticView):
    @manage_exceptions
    async def post(self, config: swarm_schemas.SwarmInit) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            swarm_id = await swarm.init_swarm(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=swarm_id,
                ).dict()
            )


class SwarmJoinView(PydanticView):
    @manage_exceptions
    async def post(self, config: swarm_schemas.SwarmJoin) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await swarm.join_swarm(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class SwarmLeaveView(PydanticView):
    @manage_exceptions
    async def post(self, force: bool = False) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await swarm.leave_swarm(docker_session=session, force=force)
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class SwarmUpdateView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            config: swarm_schemas.SwarmUpdate,
            version: int,
            rotate_worker_token: bool = False,
            rotate_manager_token: bool = False,
            rotate_manager_unlock_key: bool = False
    ) -> r200[schemas.GenericResponseModel[Mapping]]:
        async with Docker() as session:
            data = await swarm.update_swarm(
                docker_session=session,
                version=version,
                config=config.dict(),
                rotate_worker_token=rotate_worker_token,
                rotate_manager_token=rotate_manager_token,
                rotate_manager_unlock_key=rotate_manager_unlock_key
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
