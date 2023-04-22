import json
from base64 import b64encode

from aiodocker.docker import Docker

from typing import List, Mapping, MutableMapping


async def list_secrets(docker_session: Docker, filters: Mapping = None) -> List[Mapping]:
    secrets = docker_session.secrets
    secrets_list = await secrets.list(filters=filters)
    return secrets_list


async def inspect_secret(docker_session: Docker, secret_id: str) -> MutableMapping:
    secrets = docker_session.secrets
    secret = await secrets.inspect(secret_id=secret_id)
    return secret


async def get_secrets(docker_session: Docker) -> List[Mapping]:
    secrets = docker_session.secrets
    secrets_details_list = [await secrets.inspect(s['ID']) for s in await secrets.list()]

    return secrets_details_list


async def create_secret(docker_session: Docker, config: MutableMapping) -> Mapping:
    config['Data'] = b64encode(config['Data'].encode()).decode()
    config = json.dumps(config, sort_keys=True).encode("utf-8")
    response = await docker_session._query_json("secrets/create", method="POST", data=config)
    return response


async def remove_secret(docker_session: Docker, secret_id: str) -> bool:
    secrets = docker_session.secrets
    await secrets.delete(secret_id=secret_id)
    return True
