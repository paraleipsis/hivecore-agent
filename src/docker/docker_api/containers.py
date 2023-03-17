from aiodocker.channel import ChannelSubscriber
from aiodocker.containers import DockerContainer
from aiodocker.docker import Docker
from aiodocker.execs import Exec
from aiodocker.stream import Stream

from docker.docker_api.logs import DockerLogs
from aiodocker.utils import clean_filters

from typing import List, Mapping, Optional, MutableMapping

from docker.docker_api.stats import DockerStats


async def get_containers(docker_session: Docker) -> List[Mapping]:
    containers = docker_session.containers
    containers_details_list = [await DockerContainer(docker=docker_session, id=c['Id']).show()
                               for c in await containers.list(all=True)]

    return containers_details_list


async def run_container(docker_session: Docker, config: Mapping, name: Optional[str] = None) -> DockerContainer:
    container = await docker_session.containers.run(name=name, config=config)

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


async def container_attach(docker_session: Docker, container_id: str):
    pass



# import asyncio
# from client import async_docker
#
#
# async def main():
#     async with Docker() as session:
        # c = await remove_container(docker_session=session, container_id='8bffe324a788', force=True)
        # c = await run_container(docker_session=session, config={
        #         'Cmd': ['/bin/ash', '-c', 'echo "hello world"'],
        #         'Image': 'alpine:latest',
        #     })
        # c = await prune_containers(docker_session=session)
        # c = await start_container(docker_session=session, container_id='b3d88d8ce56')
        # c = await restart_container(docker_session=session, container_id='f1a64b9ca037')

        #logs
        # logs_subscriber = container_logs_subscriber(docker_session=session, container_id='da', stdout=True, stderr=True, follow=True)
        # while True:
        #     message = await logs_subscriber.get()
        #     if message is None:
        #         break
        #     print(message)
        # return None

        # #stats
        # stats_subscriber = container_stats_subscriber(docker_session=session, container_id='f27')
        # while True:
        #     message = await stats_subscriber.get()
        #     if message is None:
        #         break
        #     print(message)
        # return None

    # return c

# print(asyncio.run(main()))