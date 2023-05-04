from typing import MutableMapping

from docker.exceptions import PortsError
from docker.utils.ports import format_port_bind
from docker.utils.volumes import format_volumes_bind
from aiodocker.utils import format_env


def format_config(
        config: MutableMapping
) -> MutableMapping:
    if "Env" in config:
        config["Env"] = [
            format_env(k, v)
            for k, v in config["Env"].items()
        ]

    if "PortsBind" in config:
        if 'HostConfig' in config and 'PortBindings' in config['HostConfig']:
            raise PortsError('You need to specify either PortBindings or PortsBind')
        if 'ExposedPorts' not in config:
            config['ExposedPorts'] = {}
        if 'HostConfig' not in config:
            config['HostConfig'] = {'PortBindings': {}}
        else:
            config['HostConfig']['PortBindings'] = {}

        ports = config.pop("PortsBind")

        for port in ports:
            if not port['tcp'] and not port['udp']:
                raise PortsError('You need to specify either TCP or UDP or both')
            if port['tcp']:
                config = format_port_bind(config=config, port_mapping=port, port_type='tcp')
            if port['udp']:
                config = format_port_bind(config=config, port_mapping=port, port_type='udp')

    if "VolumesBind" in config:
        if 'HostConfig' in config and 'Binds' in config['HostConfig']:
            raise PortsError('You need to specify either Binds or VolumesBind')
        if 'Volumes' not in config:
            config['Volumes'] = {}
        if 'HostConfig' not in config:
            config['HostConfig'] = {'Binds': []}
        else:
            config['HostConfig']['Binds'] = []

            config = format_volumes_bind(config=config)

    return config
