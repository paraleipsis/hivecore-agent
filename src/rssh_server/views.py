from typing import Any

import aiohttp


async def get_resource(target_resource: str, data=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(target_resource) as resp:
            response = await resp.json()

    return response


async def post_resource(resource: str, data: Any = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(resource, data=data) as resp:
            response = await resp.json()

    return response


async def ws_resource(target_resource: str, data=None) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(target_resource) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    yield msg
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
