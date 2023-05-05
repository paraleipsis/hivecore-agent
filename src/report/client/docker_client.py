from typing import Generator, MutableMapping

from modules.client.requests_handler import get_request, establish_websocket_conn
from report.utils import format_response, format_image_id, format_volume_id


async def get_docker_images() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/images/inspect')
    images = format_response(key='images', response=response)

    for image in images['images']['data']:
        format_image_id(image)

    return images


async def get_docker_containers() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/containers/inspect')
    containers = format_response(key='containers', response=response)
    return containers


async def get_docker_volumes() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/volumes/inspect')
    volumes = format_response(key='volumes', response=response)

    for volume in volumes['volumes']['data']:
        format_volume_id(volume)

    return volumes


async def get_docker_networks() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/networks/inspect')
    networks = format_response(key='networks', response=response)
    return networks


async def get_docker_system() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/system')
    system = format_response(key='system', response=response)
    return system


async def get_docker_df() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/system/df')
    df = format_response(key='df', response=response)
    return df


async def get_docker_version() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/version')
    version = format_response(key='version', response=response)
    return version


async def get_docker_plugins() -> MutableMapping:
    response = await get_request(url='http://127.0.0.1:8080/docker/plugins/inspect')
    plugins = format_response(key='plugins', response=response)
    return plugins


async def ws_docker_events() -> Generator[MutableMapping, MutableMapping, None]:
    async for event in establish_websocket_conn(
            url='http://127.0.0.1:8080/docker/system/events'
    ):
        yield event
