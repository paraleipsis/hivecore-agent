from aiodocker.docker import Docker
from aiodocker.networks import DockerNetwork

from typing import List, Mapping, MutableMapping, Dict

from aiodocker.utils import clean_filters


async def list_networks(
        docker_session: Docker,
        filters: Mapping = None
) -> List[Mapping]:
    params = {"filters": clean_filters(filters)}
    networks = await docker_session._query_json(
        "networks",
        "GET",
        params=params
    )
    return networks


async def inspect_network(
        docker_session: Docker,
        network_id: str,
        verbose: bool = False,
        scope: str = None
) -> List[Mapping]:
    params = {
        "verbose": verbose,
        "scope": scope
    }
    network = await docker_session._query_json(
        "networks/{network_id}".format(network_id=network_id),
        "GET",
        params=params
    )
    return network


async def get_networks(
        docker_session: Docker
) -> List[Mapping]:
    networks = docker_session.networks
    networks_details_list = [
        await DockerNetwork(
            docker=docker_session,
            id_=n['Id']
        ).show() for n in await networks.list()
    ]

    return networks_details_list


async def create_network(
        docker_session: Docker,
        config: Mapping
) -> DockerNetwork:
    network = await docker_session.networks.create(config=config)

    return network


async def prune_networks(
        docker_session: Docker,
        filters: Mapping = None
) -> MutableMapping:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json(
        "networks/prune",
        method="POST",
        params=params
    )

    return response


async def remove_network(
        docker_session: Docker,
        network_id: str
) -> bool:
    await DockerNetwork(
        docker=docker_session,
        id_=network_id
    ).delete()

    return True


async def connect_container_to_network(
        docker_session: Docker,
        network_id,
        config: Dict
) -> bool:
    await DockerNetwork(
        docker=docker_session,
        id_=network_id
    ).connect(config=config)

    return True


async def disconnect_container_from_network(
        docker_session: Docker,
        network_id, config: Dict
) -> bool:
    await DockerNetwork(
        docker=docker_session,
        id_=network_id
    ).disconnect(config=config)

    return True
