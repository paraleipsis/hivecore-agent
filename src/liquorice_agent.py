import pathlib

from aiohttp import web
from config.utils import load_config

BASE_DIR = pathlib.Path(__file__).parent


def setup_routes(application):
    from docker.router import setup_routes as setup_docker_routes

    setup_docker_routes(application)


def init():
    conf = load_config(BASE_DIR / 'config' / 'config.yml')

    app = web.Application()

    setup_routes(app)

    host, port = conf['host'], conf['port']
    return app, host, port


def main():
    # logging.basicConfig(level=logging.DEBUG)

    app, host, port = init()
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
