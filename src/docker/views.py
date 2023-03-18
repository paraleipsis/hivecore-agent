# придумать как запускать задачу на фоне и при этом отдавать резльатт ее выполнения
# запустить сервер с одним эндпоинтом
# поместить в него таску на бекграунд
# попытаться сделать пару запросов и посмотреть результат
# если оба запроса выполнятся за одинаковое время знаичт все ок
# если нет значит идет выполнение сначала одного запроса потом второго - думать над другим решением
import asyncio
from typing import Mapping, MutableMapping, List, Optional, Union

from aiodocker import DockerError, Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from docker.docker_api import containers
from docker import schemas
from aiohttp_pydantic.oas.typing import r200

from docker.schemas import ContainerCreate


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
                data=schemas.GenericResponseModel(success=False, error_msg=str(e)).dict()
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
    async def post(self, config: ContainerCreate, name: Optional[str] = None,
                   auth: Optional[Union[Mapping, str, bytes]] = None) -> r200[schemas.GenericResponseModel[str]]:
        try:
            async with Docker() as session:
                data = await containers.run_container(
                    docker_session=session,
                    config=config.dict(),
                    auth=auth,
                    name=name
                )
                return web.json_response(
                    data=schemas.GenericResponseModel(
                        data=data.id,
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
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.start_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerStopView(PydanticView):
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.stop_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerRestartView(PydanticView):
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.restart_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerPauseView(PydanticView):
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.pause_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerUnpauseView(PydanticView):
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.unpause_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerKillView(PydanticView):
    async def post(self, container_id: str) -> r200[schemas.GenericResponseModel[bool]]:
        try:
            async with Docker() as session:
                data = await containers.kill_container(
                    docker_session=session,
                    container_id=container_id,
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


class ContainerLogsView(PydanticView):
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        # self.request.app['websockets'].append(ws)

        try:
            async with Docker() as session:
                logs_subscriber = containers.container_logs_subscriber(
                    docker_session=session,
                    container_id=container_id,
                    stdout=True,
                    stderr=True,
                    follow=True
                )
                while True:
                    message = await logs_subscriber.get()
                    if message is None:
                        break
                    await ws.send_str(str(message))
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
        finally:
            await ws.close()
            # self.request.app['websockets'].remove(ws)
            return ws


class ContainerStatsView(PydanticView):
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        # self.request.app['websockets'].append(ws)

        try:
            async with Docker() as session:
                stats_subscriber = containers.container_stats_subscriber(
                    docker_session=session,
                    container_id=container_id,
                )
                while True:
                    message = await stats_subscriber.get()
                    if message is None:
                        break
                    await ws.send_str(str(message))
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
        finally:
            await ws.close()
            # self.request.app['websockets'].remove(ws)
            return ws


class ContainerTerminalView(PydanticView):
    async def get(self, container_id: str, /):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        # self.request.app['websockets'].append(ws)

        try:
            async with Docker() as session:
                terminal_session = await containers.container_terminal(
                    docker_session=session,
                    container_id=container_id
                )
                async with terminal_session as terminal:
                    task1 = asyncio.create_task(containers.read_terminal(terminal_session=terminal, ws=ws))
                    task2 = asyncio.create_task(containers.write_terminal(terminal_session=terminal, ws=ws))
                    await asyncio.gather(task1, task2)
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
        finally:
            await ws.close()
            # self.request.app['websockets'].remove(ws)
            return ws


class ContainerAttachView(PydanticView): # ws

    async def get(self):
        return
