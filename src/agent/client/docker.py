from typing import MutableMapping

import aiohttp
from agent.agent_config import (DOCKER_PING_URL, SERVER_URL)


async def ping_docker() -> MutableMapping:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f'{SERVER_URL}/{DOCKER_PING_URL}')
        resp_data = await resp.json()

    return resp_data
