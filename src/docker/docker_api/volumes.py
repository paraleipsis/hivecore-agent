from aiodocker.utils import clean_filters
from aiodocker.volumes import DockerVolume
from aiodocker.docker import Docker

from typing import List, Mapping, MutableMapping

from operator import itemgetter


async def get_volumes(docker_session: Docker) -> List[Mapping]:
    volumes = docker_session.volumes
    volumes, warnings = itemgetter('Volumes', 'Warnings')(await volumes.list())
    volumes_details_list = [await DockerVolume(docker=docker_session, name=v['Name']).show()
                            for v in volumes]

    return volumes_details_list


async def create_volume(docker_session: Docker, config: Mapping) -> DockerVolume:
    volume = await docker_session.volumes.create(config=config)

    return volume


async def prune_volumes(docker_session: Docker, filters: Mapping = None) -> MutableMapping:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json("volumes/prune", method="POST", params=params)
    return response


async def remove_volume(docker_session: Docker, name: str) -> bool:
    await DockerVolume(docker=docker_session, name=name).delete()
    return True
