from typing import MutableMapping

from agent.client.docker import ping_docker


async def get_active_platforms() -> MutableMapping:
    active_platforms = {}
    docker = await ping_docker()
    if docker['data'] == 'OK':
        active_platforms['docker'] = True

    return active_platforms
