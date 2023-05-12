from typing import MutableMapping

import aiohttp
from agent.conf import (DOCKER_PING, AGENT_URL)


async def ping_docker() -> MutableMapping:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f'{AGENT_URL}/{DOCKER_PING}')
        resp_data = await resp.json()

    return resp_data
