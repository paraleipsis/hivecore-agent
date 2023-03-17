from aiodocker.docker import Docker

from typing import List, Mapping


async def get_nodes(docker_session: Docker) -> List[Mapping]:
    nodes = docker_session.nodes
    nodes_details_list = [await nodes.inspect(node_id=n['ID']) for n in await nodes.list()]

    return nodes_details_list
