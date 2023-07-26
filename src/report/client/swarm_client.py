from typing import MutableMapping

from modules.client.request_handler import ClientRequestHandler
from report.utils import format_response
from report.report_config import (SERVER_URL, SWARM_ENDPOINT, SERVICES_INSPECT, TASKS_INSPECT, CONFIGS_INSPECT,
                                  SECRETS_INSPECT, NODES_INSPECT)


async def get_swarm(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}'
    )
    response = await response.json()
    swarm = format_response(
        key='swarm',
        response=response
    )

    return swarm


async def get_swarm_services(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}/{SERVICES_INSPECT}'
    )
    response = await response.json()
    services = format_response(
        key='services',
        response=response
    )

    return services


async def get_swarm_tasks(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}/{TASKS_INSPECT}'
    )
    response = await response.json()
    tasks = format_response(
        key='tasks',
        response=response
    )

    return tasks


async def get_swarm_configs(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}/{CONFIGS_INSPECT}'
    )
    response = await response.json()
    configs = format_response(
        key='configs',
        response=response
    )

    return configs


async def get_swarm_secrets(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}/{SECRETS_INSPECT}'
    )
    response = await response.json()
    secrets = format_response(
        key='secrets',
        response=response
    )

    return secrets


async def get_swarm_nodes(
        client: ClientRequestHandler
) -> MutableMapping:
    response = await client.get_request(
        url=f'{SERVER_URL}/{SWARM_ENDPOINT}/{NODES_INSPECT}'
    )
    response = await response.json()
    nodes = format_response(
        key='nodes',
        response=response
    )

    return nodes
