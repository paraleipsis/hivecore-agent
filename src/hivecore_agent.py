import pathlib
from typing import Tuple

from aiohttp import web
from core.config.utils import load_config
from core.startup_tasks.run_rssh import run_rssh_server
from core.router import init_routes


BASE_DIR = pathlib.Path(__file__).parent


def init() -> Tuple[web.Application, str, int]:
    conf = load_config(BASE_DIR / 'core/config' / 'config.yml')

    app = web.Application()

    app.on_startup.append(run_rssh_server)

    init_routes(app)

    host, port = conf['host'], conf['port']

    return app, host, port


def main() -> None:
    app, host, port = init()

    web.run_app(app, host=host, port=port)

    return None


if __name__ == '__main__':
    main()
