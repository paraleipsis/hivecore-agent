from typing import MutableMapping


def format_port_bind(
        port_mapping: MutableMapping,
        config: MutableMapping,
        port_type: str
) -> MutableMapping:

    c_port = f"{port_mapping['container_port']}/{port_type.lower()}"
    config['ExposedPorts'][c_port] = {}
    if isinstance(port_mapping['host_port'], list):
        h_ports = [{'HostPort': i} for i in port_mapping['host_port']]
        config['HostConfig']['PortBindings'][c_port] = h_ports
    else:
        config['HostConfig']['PortBindings'][c_port] = [{'HostPort': port_mapping['host_port']}]

    return config
