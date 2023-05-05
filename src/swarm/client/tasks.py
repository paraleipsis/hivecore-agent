from aiodocker.docker import Docker
from aiodocker.channel import ChannelSubscriber

from swarm.client.logs import SwarmLogs, SwarmObjectURL

from typing import List, Mapping, MutableMapping


async def list_tasks(docker_session: Docker, filters: Mapping = None) -> List[Mapping]:
    tasks = docker_session.tasks
    tasks_list = await tasks.list(filters=filters)
    return tasks_list


async def inspect_task(docker_session: Docker, task_id: str) -> MutableMapping:
    tasks = docker_session.tasks
    task = await tasks.inspect(task_id=task_id)
    return task


async def get_tasks(docker_session: Docker) -> List[Mapping]:
    tasks = docker_session.tasks
    tasks_details_list = [await tasks.inspect(t['ID']) for t in await tasks.list()]

    return tasks_details_list


def task_logs_subscriber(docker_session: Docker, task_id: str, **kwargs) -> ChannelSubscriber:
    logs = SwarmLogs(docker=docker_session, swarm_object=SwarmObjectURL.TASK, object_id=task_id)
    logs_subscriber = logs.subscribe(**kwargs)
    return logs_subscriber
