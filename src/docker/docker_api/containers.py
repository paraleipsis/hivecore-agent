from aiodocker import DockerError, DockerContainerError
from aiodocker.channel import ChannelSubscriber
from aiodocker.containers import DockerContainer, DockerContainers
from aiodocker.docker import Docker
from aiodocker.execs import Exec
from aiodocker.stream import Stream
from aiohttp.web_ws import WebSocketResponse

from docker.docker_api.images import pull_image
from docker.docker_api.logs import DockerLogs
from aiodocker.utils import clean_filters

from typing import List, Mapping, Optional, MutableMapping, Union

from docker.docker_api.stats import DockerStats


async def list_containers(docker_session: Docker, list_all: bool = False, size: bool = False,
                          filters: Mapping = None) -> List[Mapping]:
    params = {"filters": clean_filters(filters), "all": list_all, "size": size}
    containers = await docker_session._query_json("containers/json", method="GET", params=params)
    return containers


async def inspect_container(docker_session: Docker, container_id: str, size: bool = False) -> MutableMapping:
    params = {"size": size}
    container = await docker_session._query_json(
        "containers/{container_id}/json".format(container_id=container_id),
        method="GET",
        params=params
    )
    return container


async def get_containers(docker_session: Docker) -> List[Mapping]:
    containers = await list_containers(docker_session=docker_session, list_all=True)
    containers_details_list = [
        await inspect_container(
            docker_session=docker_session,
            container_id=c['Id'],
            size=True
        )
        for c in containers
    ]

    return containers_details_list


async def run_container(docker_session: Docker, config, auth: Optional[Union[Mapping, str, bytes]] = None,
                        name: Optional[str] = None) -> DockerContainer:
    try:
        container = await create_container(docker_session=docker_session, config=config, name=name)
    except DockerError as err:
        # image not found, try pulling it
        if err.status == 404 and "Image" in config:
            tag = None
            if ":" in config["Image"]:
                tag = config["Image"].split(":")[1]
            await pull_image(from_image=config["Image"], tag=tag, docker_session=docker_session, auth=auth)
            container = await create_container(docker_session=docker_session, config=config, name=name)
        else:
            raise err

    try:
        await container.start()
    except DockerError as err:
        raise DockerContainerError(
            err.status, {"message": err.message}, container["id"]
        )

    return container


async def remove_container(docker_session: Docker, container_id: str,
                           v: bool = False, link: bool = False, force: bool = False) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).delete(v=v, link=link, force=force)
    return True


async def prune_containers(docker_session: Docker, filters: Mapping = None) -> MutableMapping:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json("containers/prune", method="POST", params=params)
    return response


async def start_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).start()
    return True


async def pause_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).pause()
    return True


async def restart_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).restart()
    return True


async def unpause_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).unpause()
    return True


async def kill_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).kill()
    return True


async def stop_container(docker_session: Docker, container_id: str) -> bool:
    await DockerContainer(docker=docker_session, id=container_id).stop()
    return True


def container_logs_subscriber(docker_session: Docker, container_id: str, **kwargs) -> ChannelSubscriber:
    logs = DockerLogs(docker=docker_session, container_id=container_id)
    logs_subscriber = logs.subscribe(**kwargs)
    return logs_subscriber


def container_stats_subscriber(docker_session: Docker, container_id: str) -> ChannelSubscriber:
    stats = DockerStats(docker=docker_session, container_id=container_id)
    stats_subscriber = stats.subscribe()
    return stats_subscriber


async def read_terminal(terminal_session: Stream, ws: WebSocketResponse):
    while not ws.closed:
        output = await terminal_session.read_out()
        await ws.send_str(str(output.data, encoding='utf8'))


async def write_terminal(terminal_session: Stream, ws: WebSocketResponse):
    async for msg in ws:
        cmd = bytes(msg.data + '\r\n', encoding='utf8')
        await terminal_session.write_in(cmd)


async def container_terminal(docker_session: Docker, container_id: str) -> Stream:
    params = {"AttachStdin": True,
              "AttachStdout": True,
              "AttachStderr": True,
              "Tty": True,
              "Cmd": [
                    "/bin/sh",
                    "-c",
                    'TERM=xterm-256color; export TERM; '
                    '[ -x /bin/bash ] && ([ -x /usr/bin/script ] && /usr/bin/script -q -c "/bin/bash" /dev/null || '
                    'exec /bin/bash) || exec /bin/sh']}
    exec_create = await docker_session._query_json(
        "containers/{container_id}/exec".format(container_id=container_id),
        method="POST",
        data=params
    )
    exec_instance = Exec(docker=docker_session, id=exec_create['Id'], tty=True)
    return exec_instance.start()


async def create_container(docker_session: Docker, config, name=None) -> DockerContainer:
    container = await DockerContainers(docker=docker_session).create(config=config, name=name)
    return container


async def attach_container(docker_session: Docker, container_id: str):
    pass


# import asyncio
#
# async def main():
#     async with Docker() as session:
#         # logs
#         logs_subscriber = container_logs_subscriber(docker_session=session, container_id='da', stdout=True, stderr=True, follow=True)
#         while True:
#             message = await logs_subscriber.get()
#             if message is None:
#                 break
#             print(message)
#         return None
#
#     # return c
#
# print(asyncio.run(main()))