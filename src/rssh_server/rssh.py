from modules.rssh.server.server import ReverseSSHServer
from rssh_server.conf import (REMOTE_HOST, REMOTE_PORT, SERVER_HOST_KEYS, SSH_ENCODING,
                              AUTHORIZED_KEYS, HOST_UUID, SSH_CONNECTION_TIMEOUT)


def setup_routes(reverse_ssh_server: ReverseSSHServer) -> None:
    from rssh_server.router import setup_routes as setup_ssh_routes

    setup_ssh_routes(reverse_ssh_server)


def init_rssh_server() -> ReverseSSHServer:
    rserver = ReverseSSHServer(
        remote_host=REMOTE_HOST,
        remote_port=REMOTE_PORT,
        server_host_keys=SERVER_HOST_KEYS,
        authorized_client_keys=AUTHORIZED_KEYS,
        encoding=SSH_ENCODING,
        server_uuid=HOST_UUID,
        connection_timeout=SSH_CONNECTION_TIMEOUT
    )

    setup_routes(rserver)

    return rserver


rssh_server = init_rssh_server()
