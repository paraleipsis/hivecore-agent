import asyncio
import warnings
from collections import ChainMap

import aiohttp

from aiodocker.channel import Channel

from swarm.schemas.services_schemas import SwarmObjectURL


class SwarmLogs:
    def __init__(self, docker, swarm_object: SwarmObjectURL, object_id: str):
        self.docker = docker
        self.channel = Channel()
        self.swarm_object = swarm_object
        self.object_id = object_id
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
                self.swarm_object.format(object_id=self.object_id), method="GET", params=params, timeout=0
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
