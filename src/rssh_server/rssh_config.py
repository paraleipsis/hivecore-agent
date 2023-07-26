from uuid import UUID

import trafaret as t

from config.config import CONFIGS_BASE_DIR
from config.utils import load_config

CONFIG_FILE = 'rssh_server_config.yml'
SSH_CONFIG_FILE = 'ssh_keys_config.yml'
AGENT_CONFIG_FILE = 'agent_config.yml'

CONFIG_TRAFARET = t.Dict(
    {
        'SSH_CLIENT_LOCAL_HOST': t.IP,
        'SSH_CLIENT_LOCAL_PORT': t.Int(),
        'SSH_CLIENT_REMOTE_HOST': t.IP,
        'SSH_CLIENT_REMOTE_PORT': t.Int(),
        'SSH_ENCODING': t.String,
        'SSH_CONNECTION_TIMEOUT': t.Int(),
        'SSH_ALG_NAME': t.String,
    }
)

SSH_CONFIG_TRAFARET = t.Dict(
    {
        'SSH_PRIVATE_KEY_PATH': t.String,
        'SSH_AUTHORIZED_KEYS_PATH': t.String,
        'SSH_PUBLIC_KEY_PATH': t.String,
    }
)

AGENT_CONFIG_TRAFARET = t.Dict(
    {
        'UUID': UUID,
        'TOKEN': t.String,
        'DOCKER_PING_URL': t.String,
    }
)

CONF = load_config(
    file=CONFIGS_BASE_DIR / CONFIG_FILE,
    config_trafaret=CONFIG_TRAFARET
)

SSH_CONF = load_config(
    file=CONFIGS_BASE_DIR / SSH_CONFIG_FILE,
    config_trafaret=SSH_CONFIG_TRAFARET
)

AGENT_CONF = load_config(
    file=CONFIGS_BASE_DIR / AGENT_CONFIG_FILE,
    config_trafaret=AGENT_CONFIG_TRAFARET
)

LOCAL_HOST = CONF['SSH_CLIENT_LOCAL_HOST']
LOCAL_PORT = CONF['SSH_CLIENT_LOCAL_PORT']
REMOTE_HOST = CONF['SSH_CLIENT_REMOTE_HOST']
REMOTE_PORT = CONF['SSH_CLIENT_REMOTE_PORT']
SSH_ENCODING = CONF['SSH_ENCODING']
SSH_CONNECTION_TIMEOUT = CONF['SSH_CONNECTION_TIMEOUT']
SSH_ALG_NAME = CONF['SSH_ALG_NAME']

SSH_PRIVATE_KEY_PATH = str(CONFIGS_BASE_DIR / SSH_CONF['SSH_PRIVATE_KEY_PATH'])
SSH_PUBLIC_KEY_PATH = str(CONFIGS_BASE_DIR / SSH_CONF['SSH_PUBLIC_KEY_PATH'])
AUTHORIZED_KEYS_PATH = str(CONFIGS_BASE_DIR / SSH_CONF['SSH_AUTHORIZED_KEYS_PATH'])
SSH_SERVER_CONFIG_PATH = str(CONFIGS_BASE_DIR / CONFIG_FILE)

HOST_UUID = AGENT_CONF['UUID']
HOST_TOKEN = AGENT_CONF['TOKEN']
