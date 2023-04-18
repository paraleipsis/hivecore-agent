import asyncio

import asyncssh
import sys
import logging
from session import ReverseSSHServerSession


class ReverseSSHServer(asyncssh.SSHServer):
    REQUEST_TYPES = ('GET', 'POST', 'UPDATE', 'DELETE')
    STREAM_TYPES = ('WS',)
    ALL_TYPES = REQUEST_TYPES + STREAM_TYPES

    _callbacks = {request_type: dict() for request_type in ALL_TYPES}

    def __init__(
            self,
            remote_host: str,
            remote_port: int,
            server_host_keys: str,
            authorized_client_keys: str,
            encoding: str = None
    ):
        """Instantiate an SSH server that listens on the given port for clients that match the authorized keys"""

        self.remote_host = remote_host
        self.remote_port = remote_port
        self._server_host_keys = [server_host_keys]
        self._authorized_client_keys = authorized_client_keys
        self._encoding = encoding

    def connection_requested(
            self,
            dest_host: str,
            dest_port: int,
            orig_host: str,
            orig_port: int
    ) -> asyncssh.SSHTCPSession:

        logging.info(f"Connection requested {dest_host} {dest_port} {orig_host} {orig_port}")
        return ReverseSSHServerSession(
            callbacks=ReverseSSHServer._callbacks,
            request_types=ReverseSSHServer.REQUEST_TYPES,
            stream_types=ReverseSSHServer.STREAM_TYPES
        )

    async def __create_server(self) -> None:
        """Make an outbound connection and then become an SSH server on it"""
        conn = await asyncssh.connect_reverse(
            host=self.remote_host,
            port=self.remote_port,
            server_host_keys=self._server_host_keys,
            authorized_client_keys=self._authorized_client_keys,
            encoding=self._encoding,
            server_factory=ReverseSSHServer
        )

        await conn.wait_closed()

    @staticmethod
    def add_callback(request_type: str, resource: str, callback: callable) -> None:
        """Configure a callable to execute when receiving a request with the given verb and resource combination"""

        if request_type not in ReverseSSHServer.ALL_TYPES:
            raise ValueError(f"Request type must be one of {ReverseSSHServer.ALL_TYPES}")

        if resource not in ReverseSSHServer._callbacks[request_type]:
            ReverseSSHServer._callbacks[request_type][resource] = callback

    # should run as a background task on aiohttp server startup
    # move __create_server outside and pass as coro in asyncio.create_task
    def start(self) -> None:
        """Start the server"""

        logging.info(f"Listening on port {self.remote_port}")

        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.__create_server())

        except (OSError, asyncssh.Error) as exc:
            sys.exit(f'Reverse SSH connection failed: {exc}')
