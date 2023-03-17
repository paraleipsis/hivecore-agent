from aiodocker.docker import Docker

from typing import List, Mapping


async def get_secrets(docker_session: Docker) -> List[Mapping]:
    secrets = docker_session.secrets
    secrets_details_list = [await secrets.inspect(s['ID']) for s in await secrets.list()]

    return secrets_details_list
