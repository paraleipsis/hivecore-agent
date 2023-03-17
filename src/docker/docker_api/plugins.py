from aiodocker import Docker
from aiodocker.utils import clean_filters
from typing import Mapping, List, Any


async def list_plugins(docker_session: Docker, filters: Mapping = None) -> List[Mapping]:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json("plugins", method="GET", params=params)
    return response


async def inspect_plugin(docker_session: Docker, plugin_id: str) -> Mapping[str, Any]:
    response = await docker_session._query_json(
        "plugins/{name}/json".format(name=plugin_id), method="GET"
    )
    return response


async def get_plugins(docker_session: Docker) -> List[Mapping]:
    plugins = await list_plugins(docker_session=docker_session)
    plugins_details_list = [await inspect_plugin(docker_session=docker_session, plugin_id=n['Id']) for n in plugins]

    return plugins_details_list


async def remove_plugin(docker_session: Docker, name: str, force: bool = False) -> bool:
    params = {"force": force}
    await docker_session._query_json("plugins/{name}".format(name=name), method="DELETE", params=params)
    return True


async def install_plugin(docker_session: Docker, remote: str, name: str = None) -> bool:
    params = {"remote": remote, "name": name}
    await docker_session._query_json("plugins/pull".format(name=name), method="POST", params=params)
    return True


async def enable_plugin(docker_session: Docker, name: str, timeout: int = 0) -> bool:
    params = {"timeout": timeout}
    await docker_session._query_json("plugins/{name}/enable".format(name=name), method="POST", params=params)
    return True


async def disable_plugin(docker_session: Docker, name: str) -> bool:
    await docker_session._query_json("plugins/{name}/disable".format(name=name), method="POST")
    return True
