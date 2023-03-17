from aiodocker.docker import Docker

from typing import Mapping


async def get_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    swarm_details = await swarm.inspect()

    return swarm_details
