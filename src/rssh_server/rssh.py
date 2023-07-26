import asyncssh
import jwt
from asyncssh import SSHKey

from modules.rssh.server.server import ReverseSSHServer
from modules.utils.yaml_utils import get_yaml_data, write_yaml_data
from rssh_server.rssh_config import (REMOTE_HOST, REMOTE_PORT, SSH_PRIVATE_KEY_PATH, SSH_ENCODING,
                                     AUTHORIZED_KEYS_PATH, HOST_UUID, SSH_CONNECTION_TIMEOUT, HOST_TOKEN, SSH_ALG_NAME,
                                     SSH_PUBLIC_KEY_PATH, LOCAL_HOST, LOCAL_PORT, SSH_SERVER_CONFIG_PATH)


def setup_routes(reverse_ssh_server: ReverseSSHServer) -> None:
    from rssh_server.router import setup_routes as setup_ssh_routes

    setup_ssh_routes(reverse_ssh_server)


def generate_ssh_keys(
        alg_name: str = SSH_ALG_NAME,
        private_key_path: str = SSH_PRIVATE_KEY_PATH,
        public_key_path: str = SSH_PUBLIC_KEY_PATH
) -> SSHKey:
    skey = asyncssh.generate_private_key(alg_name)

    skey.write_private_key(private_key_path)
    skey.write_public_key(public_key_path)

    return skey


def configure_authorized_keys(
        jwt_token: str = HOST_TOKEN
) -> None:
    decoded_token = jwt.decode(
        jwt=jwt_token,
        options={
            "verify_signature": False
        }
    )

    client_public_key = decoded_token['server_pub_key']

    with open(file=AUTHORIZED_KEYS_PATH, mode='w') as f:
        f.write(client_public_key)

    return None


def configure_server_ip(
        jwt_token: str = HOST_TOKEN
) -> None:
    decoded_token = jwt.decode(
        jwt=jwt_token,
        options={
            "verify_signature": False
        }
    )

    server_ipv4 = decoded_token['server_ipv4']

    data = get_yaml_data(file=SSH_SERVER_CONFIG_PATH)
    data['SSH_CLIENT_REMOTE_HOST'] = server_ipv4

    write_yaml_data(file=SSH_SERVER_CONFIG_PATH, data=data)

    return None


def init_rssh_server() -> ReverseSSHServer:
    rserver = ReverseSSHServer(
        remote_host=REMOTE_HOST,
        remote_port=REMOTE_PORT,
        local_port=LOCAL_PORT,
        local_addr=LOCAL_HOST,
        server_host_keys=SSH_PRIVATE_KEY_PATH,
        authorized_client_keys=AUTHORIZED_KEYS_PATH,
        encoding=SSH_ENCODING,
        server_uuid=HOST_UUID,
        server_token=HOST_TOKEN,
        connection_timeout=SSH_CONNECTION_TIMEOUT
    )

    setup_routes(rserver)

    return rserver


rssh_server = init_rssh_server()
