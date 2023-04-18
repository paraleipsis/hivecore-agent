import asyncio
import logging
import pathlib
from typing import Tuple

from aiohttp import web
from config.utils import load_config

from rssh_server import liquorice_rssh_server


BASE_DIR = pathlib.Path(__file__).parent


def setup_routes(application: web.Application) -> None:
    from docker.router import setup_routes as setup_docker_routes
    from swarm.router import setup_routes as setup_swarm_routes

    setup_docker_routes(application)
    setup_swarm_routes(application)


async def create_rssh_server(application: web.Application):
    rssh_server = liquorice_rssh_server.init()

    application['rssh_server'] = asyncio.create_task(rssh_server.start())


def init() -> Tuple[web.Application, str, int]:
    conf = load_config(BASE_DIR / 'config' / 'config.yml')

    app = web.Application()

    app.on_startup.append(create_rssh_server)

    setup_routes(app)

    host, port = conf['host'], conf['port']
    return app, host, port


def main() -> None:
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

    app, host, port = init()

    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
