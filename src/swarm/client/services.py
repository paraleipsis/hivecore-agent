from aiodocker.docker import Docker
from aiodocker.utils import clean_filters
from aiodocker.channel import ChannelSubscriber

from typing import List, Mapping, MutableMapping

from swarm.client.logs import SwarmLogs, SwarmObjectURL


async def list_services(docker_session: Docker, filters: Mapping = None, status: bool = False) -> List[Mapping]:
    params = {"filters": clean_filters(filters), "status": status}

    services_list = await docker_session._query_json(
        "services", method="GET", params=params
    )
    return services_list


async def inspect_service(docker_session: Docker, service_id: str) -> MutableMapping:
    services = docker_session.services
    service = await services.inspect(service_id=service_id)
    return service


async def get_services(docker_session: Docker) -> List[Mapping]:
    services = docker_session.services
    services_details_list = [await services.inspect(s['ID']) for s in await services.list()]

    return services_details_list


async def create_service(docker_session: Docker, config: MutableMapping) -> Mapping:
    services = docker_session.services
    service = await services.create(**config)
    return service


async def remove_service(docker_session: Docker, service_id: str) -> bool:
    services = docker_session.services
    await services.delete(service_id=service_id)
    return True


def service_logs_subscriber(docker_session: Docker, service_id: str, **kwargs) -> ChannelSubscriber:
    logs = SwarmLogs(docker=docker_session, swarm_object=SwarmObjectURL.SERVICE, object_id=service_id)
    logs_subscriber = logs.subscribe(**kwargs)
    return logs_subscriber

