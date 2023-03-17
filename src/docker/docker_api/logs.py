import asyncio
import warnings
from collections import ChainMap
import aiohttp

from aiodocker.channel import Channel


class DockerLogs:
    def __init__(self, docker, container_id: str):
        self.docker = docker
        self.channel = Channel()
        self.container_id = container_id
        self.task = None
        self.response = None

    def subscribe(self, *, create_task=True, **params):
        if create_task and not self.task:
            self.task = asyncio.ensure_future(self.run(**params))
        return self.channel.subscribe()

    async def run(self, **params):
        if self.response:
            warnings.warn(message="already running", category=RuntimeWarning, stacklevel=2)
            return
        forced_params = {"follow": True}
        default_params = {"stdout": True, "stderr": True}
        params = ChainMap(forced_params, params, default_params)
        try:
            async with self.docker._query(
                "containers/{self.container_id}/logs".format(self=self), method="GET", params=params, timeout=0
            ) as self.response:
                assert self.response is not None
                while True:
                    msg = await self.response.content.readline()
                    if not msg:
                        break
                    await self.channel.publish(msg)
        except (aiohttp.ClientConnectionError, aiohttp.ServerDisconnectedError):
            pass
        finally:
            # signal termination to subscribers
            await self.channel.publish(None)
            if self.response is not None:
                try:
                    await self.response.release()
                except Exception:
                    pass
            self.response = None

    async def stop(self):
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
