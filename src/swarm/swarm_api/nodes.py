import json

from aiodocker.docker import Docker

from typing import List, Mapping, MutableMapping


async def list_nodes(docker_session: Docker, filters: Mapping = None) -> List[Mapping]:
    nodes = docker_session.nodes
    nodes_list = await nodes.list(filters=filters)

    return nodes_list


async def inspect_node(docker_session: Docker, node_id: str) -> MutableMapping:
    nodes = docker_session.nodes
    node = await nodes.inspect(node_id=node_id)
    return node


async def get_nodes(docker_session: Docker) -> List[Mapping]:
    nodes = docker_session.nodes
    nodes_details_list = [await nodes.inspect(node_id=n['ID']) for n in await nodes.list()]

    return nodes_details_list


async def remove_node(docker_session: Docker, node_id: str) -> bool:
    nodes = docker_session.nodes
    await nodes.delete(node_id=node_id)
    return True


async def update_node(docker_session: Docker, node_id: str, spec: MutableMapping) -> bool:
    version = await inspect_node(docker_session=docker_session, node_id=node_id)
    params = {"version": version['Version']['Index']}
    spec = json.dumps(spec, sort_keys=True).encode("utf-8")
    await docker_session._query_json(
        "nodes/{node_id}/update".format(node_id=node_id),
        method="POST",
        params=params,
        data=spec,
    )
    return True
