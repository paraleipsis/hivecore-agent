import aiohttp

from typing import Any, Generator, MutableMapping

from logger.logs import logger
from rssh_server.utils import httpize


# TODO: add exceptions handling and response codes


async def get_resource(target_resource: str, params: Any = None, data: Any = None):
    try:
        params = httpize(params)
        async with aiohttp.ClientSession() as session:
            async with session.get(target_resource, params=params, data=data) as resp:
                response = await resp.json()
    except Exception as exc:
        logger['error'].error(
            f"Exception in GET request to resource '{target_resource}':\n{repr(exc)}"
        )

    return response


async def post_resource(target_resource: str, data: Any = None, params: Any = None):
    try:
        params = httpize(params)
        async with aiohttp.ClientSession() as session:
            async with session.post(target_resource, data=data, params=params) as resp:
                response = await resp.json()
    except Exception as exc:
        logger['error'].error(
            f"Exception in POST request to resource '{target_resource}':\n{repr(exc)}"
        )

    return response


async def delete_resource(target_resource: str, params: Any = None, data: Any = None):
    try:
        params = httpize(params)
        async with aiohttp.ClientSession() as session:
            async with session.delete(target_resource, params=params, data=data) as resp:
                response = await resp.json()
    except Exception as exc:
        logger['error'].error(
            f"Exception in DELETE request to resource '{target_resource}':\n{repr(exc)}"
        )

    return response


async def ws_resource(
        target_resource: str,
        params: Any = None
) -> Generator[MutableMapping, MutableMapping, None]:
    async with aiohttp.ClientSession() as session:
        try:
            params = httpize(params)
            async with session.ws_connect(target_resource, params=params) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        yield msg.data
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        yield None
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        yield None
                        break
        except Exception as exc:
            logger['error'].error(
                f"Exception in WebSocket connection to resource '{target_resource}':\n{repr(exc)}"
            )
