from aiodocker.docker import Docker

from typing import List, Mapping


async def get_tasks(docker_session: Docker) -> List[Mapping]:
    tasks = docker_session.tasks
    tasks_details_list = [await tasks.inspect(t['ID']) for t in await tasks.list()]

    return tasks_details_list
