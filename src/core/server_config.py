import trafaret as t

from config.config import CONFIGS_BASE_DIR
from config.utils import load_config

CONFIG_FILE = 'server_config.yml'


CONFIG_TRAFARET = t.Dict(
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


HOST = CONF['HOST']
PORT = CONF['PORT']
SERVER_URL = f'http://{HOST}:{PORT}'
RRSSH_PROXY = CONF['RRSSH_PROXY']
