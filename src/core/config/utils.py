from uuid import UUID

import trafaret as t
import yaml

CONFIG_TRAFARET = t.Dict(
    {
        'host': t.IP,
        'port': t.Int(),
        'ssh_client_remote_host': t.IP,
        'ssh_client_remote_port': t.Int(),
        'ssh_server_host_keys_paths': t.String,
        'ssh_authorized_client_keys_path': t.String,
        'ssh_encoding': t.String,
        'ssh_connection_timeout': t.Int(),
        'uuid': UUID
    }
)


def load_config(file):
    with open(file, 'rt') as f:
        data = yaml.safe_load(f)
    return CONFIG_TRAFARET.check(data)
