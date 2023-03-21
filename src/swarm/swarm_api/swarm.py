from aiodocker.docker import Docker

from typing import Mapping


async def init_swarm(docker_session: Docker, config: Mapping) -> str:
    response = await docker_session._query_json("swarm/init", method="POST", data=config)
    return response


async def join_swarm(docker_session: Docker, config: Mapping) -> bool:
    await docker_session._query_json("swarm/join", method="POST", data=config)
    return True


async def leave_swarm(docker_session: Docker, force: bool = False) -> bool:
    swarm = docker_session.swarm
    await swarm.leave(force=force)
    return True


async def update_swarm(
        docker_session: Docker,
        config: Mapping,
        version: int,
        rotate_worker_token: bool = False,
        rotate_manager_token: bool = False,
        rotate_manager_unlock_key: bool = False
) -> bool:
    params = {
        "version": version,
        "rotateWorkerToken": rotate_worker_token,
        "rotateManagerToken": rotate_manager_token,
        "rotateManagerUnlockKey": rotate_manager_unlock_key
    }
    await docker_session._query_json("swarm/update", method="POST", data=config, params=params)
    return True


async def inspect_swarm(docker_session: Docker) -> Mapping:
    swarm = docker_session.swarm
    swarm_details = await swarm.inspect()
    return swarm_details
