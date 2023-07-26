from aiohttp import web
from core.startup_tasks.run_rssh import (run_rssh_server, dispose_rssh_server, configure_ssh_keys)
from core.router import init_routes
from core.server_config import HOST, PORT, RRSSH_PROXY
from rssh_server.rssh import configure_authorized_keys, configure_server_ip


def init() -> web.Application:
    app = web.Application()

    init_routes(app)

    if RRSSH_PROXY:
        configure_ssh_keys()
        configure_authorized_keys()
        configure_server_ip()
        app.on_startup.append(run_rssh_server)
        app.on_shutdown.append(dispose_rssh_server)

    return app


def main() -> None:
    app = init()

    web.run_app(
        app=app,
        host=HOST,
        port=PORT
    )

    return None


if __name__ == '__main__':
    main()
