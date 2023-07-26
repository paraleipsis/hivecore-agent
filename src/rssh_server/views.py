from typing import Any, Generator, MutableMapping

from modules.client.request_handler import ClientRequestHandler
from core.server_config import SERVER_URL


async def get_resource(
        target_resource: str,
        params: Any = None,
        data: Any = None
) -> MutableMapping:
    async with ClientRequestHandler() as client:
        response = await client.get_request(
            url=f'{SERVER_URL}/{target_resource}',
            params=params,
            data=data
        )

    return await response.json()


async def post_resource(
        target_resource: str,
        data: Any = None,
        params: Any = None
) -> MutableMapping:
    async with ClientRequestHandler() as client:
        response = await client.post_request(
            url=f'{SERVER_URL}/{target_resource}',
            params=params,
            data=data
        )

    return await response.json()


async def delete_resource(
        target_resource: str,
        params: Any = None,
        data: Any = None
) -> MutableMapping:
    async with ClientRequestHandler() as client:
        response = await client.delete_request(
            url=f'{SERVER_URL}/{target_resource}',
            params=params,
            data=data
        )

    return await response.json()


async def ws_resource(
        target_resource: str,
        params: Any = None
) -> Generator[MutableMapping, MutableMapping, None]:
    async with ClientRequestHandler() as client:
        async for msg in client.establish_websocket_conn(
                url=f'{SERVER_URL}/{target_resource}',
                params=params,
        ):
            yield msg
