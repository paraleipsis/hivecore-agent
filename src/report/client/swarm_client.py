from typing import MutableMapping

from modules.client.requests_handler import get_request
from report.utils import format_response


async def get_swarm() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm')
    swarm = format_response(key='swarm', response=response)
    return swarm


async def get_swarm_services() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm/services/inspect')
    services = format_response(key='services', response=response)
    return services


async def get_swarm_tasks() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm/tasks/inspect')
    tasks = format_response(key='tasks', response=response)
    return tasks


async def get_swarm_configs() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm/configs/inspect')
    configs = format_response(key='configs', response=response)
    return configs


async def get_swarm_secrets() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm/secrets/inspect')
    secrets = format_response(key='secrets', response=response)
    return secrets


async def get_swarm_nodes() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/swarm/nodes/inspect')
    nodes = format_response(key='nodes', response=response)
    return nodes
