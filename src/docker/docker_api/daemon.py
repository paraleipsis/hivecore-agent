from aiodocker.channel import ChannelSubscriber
from aiodocker.events import DockerEvents
from aiodocker.docker import Docker

from typing import Mapping

from images import prune_images
from containers import prune_containers
from networks import prune_networks
from volumes import prune_volumes

from collections import ChainMap


def docker_events_subscriber(docker_session: Docker, **kwargs) -> ChannelSubscriber:
    events = DockerEvents(docker=docker_session)
    events_subscriber = events.subscribe(**kwargs)
    return events_subscriber


async def get_system(docker_session: Docker) -> Mapping:
    system = docker_session.system
    system_details = await system.info()

    return system_details


async def prune_system(docker_session: Docker, volumes: bool = False) -> Mapping:
    images = await prune_images(docker_session=docker_session)
    containers = await prune_containers(docker_session=docker_session)
    networks = await prune_networks(docker_session=docker_session)

    result = ChainMap(images, containers, networks)

    if volumes:
        volumes = await prune_volumes(docker_session=docker_session)
        result = ChainMap(result, volumes)

    return result


async def get_system_df(docker_session: Docker):
    pass


async def docker_login(docker_session: Docker):
    pass


async def get_version(docker_session: Docker):
    pass






# import  asyncio
# from client import async_docker
#
#
# async def main():
#     async with async_docker.async_docker_session() as session:
#         events_sub = docker_events_subscriber(docker_session=session)
#         while True:
#             message = await events_sub.get()
#             if message is None:
#                 break
#             print(message)
#         return None
#
# asyncio.run(main())
