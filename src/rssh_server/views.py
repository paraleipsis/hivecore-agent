import aiohttp

from typing import Any, Generator, MutableMapping

from logger.logs import logger


async def get_resource(target_resource: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(target_resource) as resp:
            response = await resp.json()

    return response


async def post_resource(target_resource: str, data: Any = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(target_resource, data=data) as resp:
            response = await resp.json()

    return response


async def ws_resource(
        target_resource: str
) -> Generator[MutableMapping, MutableMapping, None]:
    # TODO: add exceptions handling
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(target_resource) as ws:
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
            logger['debug'].debug(
                f"Exception in WebSocket connection to resource '{target_resource}':\n{repr(exc)}"
            )
