from typing import MutableMapping


def format_volumes_bind(
        config: MutableMapping
) -> MutableMapping:
    volumes = config.pop("VolumesBind")

    for volume in volumes:
        c_path = volume['container_path']
        h_path = volume['host_path']
        mode = volume['mode']
        config['Volumes'][c_path] = {}
        config['HostConfig']['Binds'].append(
            f'{h_path}:{c_path}:{mode}'
        )

    return config
