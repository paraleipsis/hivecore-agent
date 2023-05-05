from typing import Mapping, MutableMapping, List

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from swarm.client import nodes
from swarm.schemas import nodes_schemas
from modules.schemas import response_schemas as schemas
from modules.utils.exceptions_utils import manage_exceptions


class NodeCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            nodes_list = await nodes.list_nodes(
                docker_session=session,
                filters=filters
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=nodes_list,
                    total=len(nodes_list)
                ).dict()
            )


class NodeCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            nodes_details_list = await nodes.get_nodes(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=nodes_details_list,
                    total=len(nodes_details_list)
                ).dict()
            )


class NodeInspectView(PydanticView):
    @manage_exceptions
    async def get(self, node_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            node_details = await nodes.inspect_node(
                docker_session=session,
                node_id=node_id,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=node_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, node_id: str, /) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await nodes.remove_node(
                docker_session=session,
                node_id=node_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class NodeUpdateView(PydanticView):
    @manage_exceptions
    async def post(self, node_id: str, /, spec: nodes_schemas.NodeSpec) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await nodes.update_node(
                docker_session=session,
                node_id=node_id,
                spec=spec.dict()
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
