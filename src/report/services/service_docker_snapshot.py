from typing import Generator

from logger.logs import logger
from modules.client.request_handler import ClientRequestHandler
from modules.tasks.task_group import GatheringTaskGroup
from report.utils import format_tg_results, swarm_check
from report.client import swarm_client, docker_client
from report.schemas import schemas_docker_snapshot


async def get_docker_snapshot() -> schemas_docker_snapshot.DockerSnapshot:
    docker_snapshot = await create_docker_snapshot()

    if docker_snapshot.swarm_mode == 'active':
        if docker_snapshot.swarm_role == 'manager':
            swarm_snapshot = await create_swarm_snapshot()
            return schemas_docker_snapshot.DockerSnapshot(
                docker=docker_snapshot,
                swarm=swarm_snapshot
            )

    return schemas_docker_snapshot.DockerSnapshot(
        docker=docker_snapshot
    )


async def get_docker_snapshot_on_event() -> Generator[
    schemas_docker_snapshot.DockerSnapshot,
    schemas_docker_snapshot.DockerSnapshot,
    None
]:
    try:
        async with ClientRequestHandler() as client:
            async for _ in docker_client.ws_docker_events(client=client):
                snapshot = await get_docker_snapshot()
                yield snapshot
    except Exception as exc:
        logger['debug'].debug(
            f"Exception in docker snapshot request:\n{repr(exc)}"
        )


async def create_docker_snapshot() -> schemas_docker_snapshot.DockerObjectsSnapshot:
    async with ClientRequestHandler() as client:
        async with GatheringTaskGroup() as tg:
            tg.create_task(docker_client.get_docker_images(client=client))
            tg.create_task(docker_client.get_docker_containers(client=client))
            tg.create_task(docker_client.get_docker_volumes(client=client))
            tg.create_task(docker_client.get_docker_networks(client=client))
            tg.create_task(docker_client.get_docker_system(client=client))
            tg.create_task(docker_client.get_docker_df(client=client))
            tg.create_task(docker_client.get_docker_version(client=client))
            tg.create_task(docker_client.get_docker_plugins(client=client))

    try:
        results = format_tg_results(
            data=tg.results()
        )

        swarm_mode, swarm_role = swarm_check(
            docker_snapshot_results=results
        )

        snapshot = schemas_docker_snapshot.DockerObjectsSnapshot(
            swarm_mode=swarm_mode,
            swarm_role=swarm_role,
            **results
        )
        return snapshot
    except Exception as exc:
        logger['debug'].debug(
            f"Exception in creating Docker Snapshot:\n{repr(exc)}"
        )


async def create_swarm_snapshot() -> schemas_docker_snapshot.SwarmObjectsSnapshot:
    async with ClientRequestHandler() as client:
        async with GatheringTaskGroup() as tg:
            tg.create_task(swarm_client.get_swarm(client=client))
            tg.create_task(swarm_client.get_swarm_services(client=client))
            tg.create_task(swarm_client.get_swarm_tasks(client=client))
            tg.create_task(swarm_client.get_swarm_configs(client=client))
            tg.create_task(swarm_client.get_swarm_secrets(client=client))
            tg.create_task(swarm_client.get_swarm_nodes(client=client))

    try:
        results = format_tg_results(
            data=tg.results()
        )
        snapshot = schemas_docker_snapshot.SwarmObjectsSnapshot(**results)
        return snapshot
    except Exception as exc:
        logger['debug'].debug(
            f"Exception in creating Swarm Snapshot:\n{repr(exc)}"
        )
