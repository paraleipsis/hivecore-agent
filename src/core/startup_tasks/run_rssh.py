import asyncio

from aiohttp import web

from rssh_server.rssh import rssh_server, generate_ssh_keys


def configure_ssh_keys() -> None:
    generate_ssh_keys()
    return None


async def run_rssh_server(application: web.Application) -> None:
    application['rssh_server'] = asyncio.create_task(rssh_server.start())


async def dispose_rssh_server(application: web.Application):
    application['rssh_server'].close()
    await application['rssh_server']
