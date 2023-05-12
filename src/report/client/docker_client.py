from typing import Generator, MutableMapping

from modules.client.request_handler import ClientRequestHandler
from report.utils import format_response, format_image_id, format_volume_id


async def get_docker_images(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/images/inspect')
    response = await response.json()
    images = format_response(key='images', response=response)

    for image in images['images']['data']:
        format_image_id(image)

    return images


async def get_docker_containers(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/containers/inspect')
    response = await response.json()
    containers = format_response(key='containers', response=response)
    return containers


async def get_docker_volumes(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/volumes/inspect')
    response = await response.json()
    volumes = format_response(key='volumes', response=response)

    for volume in volumes['volumes']['data']:
        format_volume_id(volume)

    return volumes


async def get_docker_networks(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/networks/inspect')
    response = await response.json()
    networks = format_response(key='networks', response=response)
    return networks


async def get_docker_system(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/system')
    response = await response.json()
    system = format_response(key='system', response=response)
    return system


async def get_docker_df(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/system/df')
    response = await response.json()
    df = format_response(key='df', response=response)
    return df


async def get_docker_version(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/system/version')
    response = await response.json()
    version = format_response(key='version', response=response)
    return version


async def get_docker_plugins(client: ClientRequestHandler) -> MutableMapping:
    response = await client.get_request(url='http://127.0.0.1:8080/docker/plugins/inspect')
    response = await response.json()
    plugins = format_response(key='plugins', response=response)
    return plugins


async def ws_docker_events(client: ClientRequestHandler) -> Generator[MutableMapping, MutableMapping, None]:
    async for event in client.establish_websocket_conn(
            url='http://127.0.0.1:8080/docker/system/events'
    ):
        yield event
