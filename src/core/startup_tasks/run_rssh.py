import asyncio

from aiohttp import web

from rssh_server.rssh import rssh_server


async def run_rssh_server(application: web.Application) -> None:
    application['rssh_server'] = asyncio.create_task(rssh_server.start())
