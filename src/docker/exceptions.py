class DockerClientError(Exception):
    pass


class ContainerError(DockerClientError):
    pass


class PortsError(ContainerError):
    pass
