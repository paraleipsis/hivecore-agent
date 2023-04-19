import logging
import pathlib

from rssh_server.rserver.server import ReverseSSHServer
from config.utils import load_config

BASE_DIR = pathlib.Path(__file__).parent.parent


def setup_routes(reverse_ssh_server: ReverseSSHServer) -> None:
    from rssh_server.router import setup_routes as setup_ssh_routes

    setup_ssh_routes(reverse_ssh_server)


def init() -> ReverseSSHServer:
    conf = load_config(BASE_DIR / 'config' / 'config.yml')

    remote_host = conf['ssh_client_remote_host']
    remote_port = conf['ssh_client_remote_port']
    server_host_keys = conf['ssh_server_host_keys_paths']
    authorized_client_keys = conf['ssh_authorized_client_keys_path']
    ssh_encoding = conf['ssh_encoding']

    rserver = ReverseSSHServer(
        remote_host=remote_host,
        remote_port=remote_port,
        server_host_keys=server_host_keys,
        authorized_client_keys=authorized_client_keys,
        encoding=ssh_encoding
    )

    setup_routes(rserver)

    return rserver


# def main() -> None:
#     # logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')
#
#     rserver = init()
#     await rserver.start()
#
#
# if __name__ == '__main__':
#     main()
