from aiodocker.utils import clean_filters
from aiodocker.volumes import DockerVolume
from aiodocker.docker import Docker

from typing import List, Mapping, MutableMapping

from operator import itemgetter


async def list_volumes(
        docker_session: Docker,
        filters: Mapping = None
) -> List[Mapping]:
    params = {"filters": clean_filters(filters)}
    volumes = await docker_session._query_json(
        "volumes",
        "GET",
        params=params
    )

    return volumes


async def inspect_volume(
        docker_session: Docker,
        volume_id: str
) -> List[Mapping]:
    volume = await docker_session._query_json(
        "volumes/{volume_id}".format(volume_id=volume_id),
        "GET"
    )

    return volume


async def get_volumes(
        docker_session: Docker
) -> List[Mapping]:
    volumes = docker_session.volumes
    volumes, _ = itemgetter('Volumes', 'Warnings')(await volumes.list())
    volumes_details_list = [
        await DockerVolume(
            docker=docker_session,
            name=v['Name']
        ).show() for v in volumes
    ]

    return volumes_details_list


async def create_volume(
        docker_session: Docker,
        config: Mapping
) -> DockerVolume:
    volume = await docker_session.volumes.create(config=config)

    return volume


async def prune_volumes(
        docker_session: Docker,
        filters: Mapping = None
) -> MutableMapping:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json(
        "volumes/prune",
        method="POST",
        params=params
    )

    return response


async def remove_volume(
        docker_session: Docker,
        volume_id: str
) -> bool:
    await DockerVolume(
        docker=docker_session,
        name=volume_id
    ).delete()

    return True
