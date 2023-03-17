# придумать как запускать задачу на фоне и при этом отдавать резльатт ее выполнения
# запустить сервер с одним эндпоинтом
# поместить в него таску на бекграунд
# попытаться сделать пару запросов и посмотреть результат
# если оба запроса выполнятся за одинаковое время знаичт все ок
# если нет значит идет выполнение сначала одного запроса потом второго - думать над другим решением
from typing import Mapping, MutableMapping, List

from aiodocker import DockerError, Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from docker.docker_api import containers
from docker import schemas
from aiohttp_pydantic.oas.typing import r200, r201, r204, r404


class ContainerCollectionView(PydanticView):
    async def get(self, list_all: bool = False, size: bool = False,
                  filters: Mapping = None) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        try:
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
                    ).dict()
                )
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=e).dict()
            )


class ContainerCollectionInspectView(PydanticView):
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        try:
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
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=e).dict()
            )


class ContainerInspectView(PydanticView):
    async def get(self, container_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        try:
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
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=e).dict()
            )

    async def delete(self, container_id: str, /, v: bool = False, link: bool = False,
                     force: bool = False) -> r200[schemas.GenericResponseModel[bool]]:
        try:
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
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=e).dict()
            )


class ContainerRunView(PydanticView):

    async def post(self):  # run
        return


class ContainerPruneView(PydanticView):
    async def post(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        try:
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
        except DockerError as de:
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=e).dict()
            )


class ContainerStartView(PydanticView):

    async def post(self):
        return


class ContainerStopView(PydanticView):

    async def post(self):
        return


class ContainerRestartView(PydanticView):

    async def post(self):
        return


class ContainerPauseView(PydanticView):

    async def post(self):
        return


class ContainerUnpauseView(PydanticView):

    async def post(self):
        return


class ContainerKillView(PydanticView):

    async def post(self):
        return


class ContainerLogsView(PydanticView): # ws

    async def get(self):
        return


class ContainerStatsView(PydanticView): # ws

    async def get(self):
        return


class ContainerTerminalView(PydanticView): # ws

    async def get(self):
        return


class ContainerAttachView(PydanticView): # ws

    async def get(self):
        return
