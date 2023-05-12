import json

from aiodocker.channel import ChannelSubscriber
from aiodocker.events import DockerEvents
from aiodocker.docker import Docker

from typing import Mapping

from docker.client.images import prune_images
from docker.client.containers import prune_containers
from docker.client.networks import prune_networks
from docker.client.volumes import prune_volumes

from collections import ChainMap


def docker_events_subscriber(
        docker_session: Docker,
        **kwargs
) -> ChannelSubscriber:
    events = DockerEvents(docker=docker_session)
    events_subscriber = events.subscribe(**kwargs)

    return events_subscriber


async def get_system(
        docker_session: Docker
) -> Mapping:
    system = docker_session.system
    system_details = await system.info()

    return system_details


async def prune_system(
        docker_session: Docker,
        volumes: bool = False
) -> Mapping:
    images = await prune_images(docker_session=docker_session)
    containers = await prune_containers(docker_session=docker_session)
    networks = await prune_networks(docker_session=docker_session)

    result = ChainMap(images, containers, networks)

    if volumes:
        volumes = await prune_volumes(docker_session=docker_session)
        result = ChainMap(result, volumes)

    return result


async def get_system_df(
        docker_session: Docker
) -> Mapping:
    system_df = await docker_session._query_json(
        "system/df",
        "GET"
    )
    return system_df


async def docker_login(
        docker_session: Docker,
        credentials: Mapping
) -> Mapping:
    credentials = json.dumps(credentials, sort_keys=True).encode("utf-8")
    auth = await docker_session._query_json(
        "auth",
        "POST",
        data=credentials
    )

    return auth


async def get_version(
        docker_session: Docker
) -> Mapping:
    data = await docker_session._query_json(
        "version",
        "GET"
    )

    return data


async def ping(
        docker_session: Docker
) -> Mapping:
    data = await docker_session._query_json(
        "_ping",
        "GET"
    )

    return data
