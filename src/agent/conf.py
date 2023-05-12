import pathlib
from core.config.utils import load_config


BASE_DIR = pathlib.Path(__file__).parent.parent

conf = load_config(BASE_DIR / 'core/config' / 'config.yml')


HOST = conf['host']
PORT = conf['port']
AGENT_URL = f'http://{HOST}:{PORT}'
DOCKER_PING = conf['docker_ping']
