import pathlib
from core.config.utils import load_config


BASE_DIR = pathlib.Path(__file__).parent.parent

conf = load_config(BASE_DIR / 'core/config' / 'config.yml')

REMOTE_HOST = conf['ssh_client_remote_host']
REMOTE_PORT = conf['ssh_client_remote_port']
SERVER_HOST_KEYS = conf['ssh_server_host_keys_paths']
AUTHORIZED_KEYS = conf['ssh_authorized_client_keys_path']
SSH_ENCODING = conf['ssh_encoding']
HOST_UUID = conf['uuid']
SSH_CONNECTION_TIMEOUT = conf['ssh_connection_timeout']
