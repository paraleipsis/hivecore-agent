from typing import Generator, MutableMapping, Optional, Any

import aiohttp

from logger.logs import logger


async def get_request(
        url: str,
        **kwargs
) -> MutableMapping:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, **kwargs)

            if response.status != 200:
                logger['debug'].debug(
                    f"Exception in GET request to resource '{url}' - response status: {response.status}"
                )

            response_json = await response.json()

            return response_json
    except Exception as exc:
        logger['debug'].debug(
            f"Exception in GET request to resource '{url}':\n{repr(exc)}"
        )


async def post_request(
        url: str,
        data: Any = None,
        params: Optional[MutableMapping] = None,
        **kwargs
) -> MutableMapping:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=url, data=data, params=params, **kwargs)

            if response.status != 200:
                logger['debug'].debug(
                    f"Exception in POST request to resource '{url}' - response status: {response.status}"
                )

            response_json = await response.json()

            return response_json
    except Exception as exc:
        logger['debug'].debug(
            f"Exception in GET request to resource '{url}':\n{repr(exc)}"
        )


async def establish_websocket_conn(
        url: str,
        **kwargs
) -> Generator[MutableMapping, MutableMapping, None]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.ws_connect(url=url, **kwargs) as ws:
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
                f"Exception in WebSocket connection to resource '{url}':\n{repr(exc)}"
            )
