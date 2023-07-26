from uuid import UUID

import trafaret as t

from config.config import CONFIGS_BASE_DIR
from config.utils import load_config

CONFIG_FILE = 'agent_config.yml'
SERVER_CONFIG_FILE = 'server_config.yml'

CONFIG_TRAFARET = t.Dict(
    {
        'UUID': UUID,
        'TOKEN': t.String,
        'DOCKER_PING_URL': t.String,
    }
)

SERVER_CONFIG_TRAFARET = t.Dict(
    {
        'HOST': t.IP,
        'PORT': t.Int(),
        'RRSSH_PROXY': t.Bool
    }
)


CONF = load_config(
    file=CONFIGS_BASE_DIR / CONFIG_FILE,
    config_trafaret=CONFIG_TRAFARET
)

SERVER_CONF = load_config(
    file=CONFIGS_BASE_DIR / SERVER_CONFIG_FILE,
    config_trafaret=SERVER_CONFIG_TRAFARET
)


HOST = SERVER_CONF['HOST']
PORT = SERVER_CONF['PORT']
SERVER_URL = f'http://{HOST}:{PORT}'

DOCKER_PING_URL = CONF['DOCKER_PING_URL']
