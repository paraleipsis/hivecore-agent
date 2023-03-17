from aiodocker.docker import Docker

from typing import List, Mapping


async def get_services(docker_session: Docker) -> List[Mapping]:
    services = docker_session.services
    services_details_list = [await services.inspect(s['ID']) for s in await services.list()]

    return services_details_list
