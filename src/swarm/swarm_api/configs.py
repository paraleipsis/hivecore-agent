from aiodocker.docker import Docker

from typing import List, Mapping


async def get_configs(docker_session: Docker) -> List[Mapping]:
    configs = docker_session.configs
    configs_details_list = [await configs.inspect(c['ID']) for c in await configs.list()]

    return configs_details_list
