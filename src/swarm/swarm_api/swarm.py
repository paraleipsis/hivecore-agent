from aiodocker.docker import Docker

from typing import Mapping


async def init_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    pass


async def join_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    pass


async def leave_swarm(docker_session: Docker, force: bool = False) -> bool:
    swarm = docker_session.swarm
    await swarm.leave(force=force)
    return True


async def update_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    pass


async def inspect_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    swarm_details = await swarm.inspect()
    return swarm_details
