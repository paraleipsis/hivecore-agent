import logging

from rssh_server.rserver.server import ReverseSSHServer
from rssh_server.conf import (REMOTE_HOST, REMOTE_PORT, SERVER_HOST_KEYS, SSH_ENCODING, AUTHORIZED_KEYS)


def setup_routes(reverse_ssh_server: ReverseSSHServer) -> None:
    from rssh_server.router import setup_routes as setup_ssh_routes

    setup_ssh_routes(reverse_ssh_server)


def init() -> ReverseSSHServer:
    rserver = ReverseSSHServer(
        remote_host=REMOTE_HOST,
        remote_port=REMOTE_PORT,
        server_host_keys=SERVER_HOST_KEYS,
        authorized_client_keys=AUTHORIZED_KEYS,
        encoding=SSH_ENCODING,
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
