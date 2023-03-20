import json
from base64 import b64encode

from aiodocker.docker import Docker

from typing import List, Mapping, MutableMapping


async def list_configs(docker_session: Docker, filters: Mapping = None) -> List[Mapping]:
    configs = docker_session.configs
    configs_list = await configs.list(filters=filters)
    return configs_list


async def inspect_config(docker_session: Docker, config_id: str) -> MutableMapping:
    configs = docker_session.configs
    config = await configs.inspect(config_id=config_id)
    return config


async def get_configs(docker_session: Docker) -> List[Mapping]:
    configs = docker_session.configs
    configs_details_list = [await configs.inspect(c['ID']) for c in await configs.list()]

    return configs_details_list


async def create_config(docker_session: Docker, config: MutableMapping) -> Mapping:
    config['Data'] = b64encode(config['Data'].encode()).decode()
    config = json.dumps(config, sort_keys=True).encode("utf-8")
    response = await docker_session._query_json("configs/create", method="POST", data=config)
    return response


async def remove_config(docker_session: Docker, config_id: str) -> bool:
    configs = docker_session.configs
    await configs.delete(config_id=config_id)
    return True
