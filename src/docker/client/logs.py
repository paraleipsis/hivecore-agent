import asyncio
import warnings
from collections import ChainMap
import aiohttp

from aiodocker.channel import Channel, ChannelSubscriber
from aiodocker.docker import Docker

from logger.logs import logger


class DockerLogs:
    def __init__(
            self,
            docker: Docker,
            container_id: str
    ):
        self.docker = docker
        self.channel = Channel()
        self.container_id = container_id
        self.task = None
        self.response = None

    def subscribe(
            self,
            *,
            create_task=True,
            **params
    ) -> ChannelSubscriber:
        if create_task and not self.task:
            self.task = asyncio.ensure_future(self.run(**params))

        return self.channel.subscribe()

    async def run(
            self,
            **params
    ) -> None:
        if self.response:
            warnings.warn(
                message="already running",
                category=RuntimeWarning,
                stacklevel=2
            )

            return None

        forced_params = {
            "follow": True
        }
        default_params = {
            "stdout": True,
            "stderr": True
        }
        params = ChainMap(
            forced_params,
            params,
            default_params
        )

        try:
            async with self.docker._query(
                "containers/{self.container_id}/logs".format(self=self),
                method="GET",
                params=params,
                timeout=0
            ) as self.response:
                if self.response is None:
                    return None
                while True:
                    msg = await self.response.content.readline()
                    if not msg:
                        break
                    await asyncio.sleep(0.01)
                    await self.channel.publish(msg)
        except (aiohttp.ClientConnectionError, aiohttp.ServerDisconnectedError) as exc:
            logger['debug'].debug(
                f'{type(exc).__name__}: {str(exc)}'
            )
        finally:
            # signal termination to subscribers
            await self.channel.publish(None)
            if self.response is not None:
                try:
                    await self.response.release()
                except Exception as exc:
                    logger['error'].error(
                        f'{type(exc).__name__}: {str(exc)}'
                    )
            self.response = None

    async def stop(self) -> None:
        if self.response:
            await self.response.release()
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            finally:
                self.task = None
