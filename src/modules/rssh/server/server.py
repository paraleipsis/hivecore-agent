import asyncio
from uuid import UUID

import asyncssh
import sys

from modules.rssh.server.session import ReverseSSHServerSession
from logger.logs import logger


class ReverseSSHServerFactory(asyncssh.SSHServer):
    REQUEST_TYPES = ('GET', 'POST', 'UPDATE', 'DELETE')
    INTERNAL_REQUEST_TYPES = ('IDENTIFY',)
    STREAM_TYPES = ('STREAM',)
    ALL_TYPES = REQUEST_TYPES + STREAM_TYPES
    SERVER_UUID = None
    SERVER_TOKEN = None

    callbacks = {request_type: dict() for request_type in ALL_TYPES}

    def connection_requested(
            self,
            dest_host: str,
            dest_port: int,
            orig_host: str,
            orig_port: int
    ) -> asyncssh.SSHTCPSession:

        logger['info'].info(
            f'Connection requested: destination - {dest_host}:{dest_port}; original - {orig_host}:{orig_port}'
        )
        return ReverseSSHServerSession(
            callbacks=ReverseSSHServerFactory.callbacks,
            request_types=ReverseSSHServerFactory.REQUEST_TYPES,
            stream_types=ReverseSSHServerFactory.STREAM_TYPES,
            internal_request_types=ReverseSSHServerFactory.INTERNAL_REQUEST_TYPES,
            server_uuid=ReverseSSHServerFactory.SERVER_UUID,
            server_token=ReverseSSHServerFactory.SERVER_TOKEN
        )


class ReverseSSHServer:
    def __init__(
            self,
            remote_host: str,
            remote_port: int,
            server_host_keys: str,
            authorized_client_keys: str,
            local_addr: str = None,
            local_port: int = None,
            encoding: str = None,
            server_uuid: UUID = None,
            server_token: str = None,
            connection_timeout: int = None
    ):
        """Instantiate a reverse SSH server that listens on the given port
        for clients that match the authorized keys"""

        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_addr = local_addr
        self.local_port = local_port
        self._server_host_keys = [server_host_keys]
        self._authorized_client_keys = authorized_client_keys
        self._encoding = encoding
        self.connection_timeout = connection_timeout
        ReverseSSHServerFactory.SERVER_UUID = server_uuid
        ReverseSSHServerFactory.SERVER_TOKEN = server_token

    @staticmethod
    def add_callback(request_type: str, resource: str, callback: callable) -> None:
        """Configure a callable to execute when receiving a request
        with the given request type and resource combination"""

        if request_type not in ReverseSSHServerFactory.ALL_TYPES:
            raise ValueError(f"Request type must be one of {ReverseSSHServerFactory.ALL_TYPES}")

        if resource not in ReverseSSHServerFactory.callbacks[request_type]:
            ReverseSSHServerFactory.callbacks[request_type][resource] = callback

    async def __connect(self):
        conn = await asyncssh.connect_reverse(
            host=self.remote_host,
            port=self.remote_port,
            # local_addr=(self.local_addr, self.local_port),
            server_host_keys=self._server_host_keys,
            authorized_client_keys=self._authorized_client_keys,
            encoding=self._encoding,
            server_factory=ReverseSSHServerFactory,
        )

        await conn.wait_closed()

    async def start(self):
        """Make an outbound connection and then become an SSH server on it"""

        logger['info'].info(
            f"Reverse SSH Server - Listening on port {self.remote_port}"
        )
        if self.connection_timeout is not None:
            while True:
                try:
                    await self.__connect()
                except (OSError, asyncssh.Error, Exception) as exc:  # fork
                    logger['error'].error(
                        f"Reverse SSH connection failed: {exc}"
                    )
                    await asyncio.sleep(self.connection_timeout)
                    continue
        else:
            try:
                await self.__connect()
            except (OSError, asyncssh.Error, Exception) as exc:
                logger['error'].error(
                    f"Reverse SSH connection failed: {exc}"
                )
                sys.exit()
