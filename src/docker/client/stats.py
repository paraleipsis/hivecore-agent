import asyncio
import datetime as dt
import warnings
from collections import ChainMap

from aiodocker.channel import Channel
from aiodocker.jsonstream import json_stream_stream


class DockerStats:
    def __init__(self, docker, container_id):
        self.docker = docker
        self.channel = Channel()
        self.container_id = container_id
        self.json_stream = None
        self.task = None

    def subscribe(self, *, create_task=True, **params):
        if create_task and not self.task:
            self.task = asyncio.ensure_future(self.run(**params))
        return self.channel.subscribe()

    def _transform_stat(self, data):
        if "time" in data:
            data["time"] = dt.datetime.fromtimestamp(data["time"])
        return data

    async def run(self, **params):
        if self.json_stream:
            warnings.warn("already running", RuntimeWarning, stacklevel=2)
            return
        forced_params = {"stream": True}
        params = ChainMap(forced_params, params)
        try:
            async with self.docker._query(
                "containers/{container_id}/stats".format(container_id=self.container_id),
                method="GET",
                params=params,
                timeout=0
            ) as response:
                self.json_stream = json_stream_stream(response, self._transform_stat)
                try:
                    async for data in self.json_stream:
                        await self.channel.publish(data)
                finally:
                    if self.json_stream is not None:
                        await self.json_stream._close()
                    self.json_stream = None
        finally:
            # signal termination to subscribers
            await self.channel.publish(None)

    async def stop(self):
        if self.json_stream is not None:
            await self.json_stream._close()
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            finally:
                self.task = None
