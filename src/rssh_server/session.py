import asyncio
import gzip
import json
import uuid
from typing import MutableMapping, Union, Tuple

import asyncssh
import logging
import traceback

from aiohttp.http_websocket import WSMessage


class ReverseSSHServerSession(asyncssh.SSHTCPSession):
    def __init__(self, callbacks: MutableMapping, request_types: Tuple, stream_types: Tuple):
        self._callbacks = callbacks
        self.request_types = request_types
        self.stream_types = stream_types
        self._chan = None

    def connection_made(self, chan: asyncssh.SSHTCPChannel) -> None:
        """New connection established"""

        logging.debug("Connection incoming")
        self._chan = chan

    def connection_lost(self, exc: Exception) -> None:
        """Lost the connection to the client"""

        logging.debug(f"Connection lost\n{exc}")

    def session_started(self) -> None:
        """New session established successfully"""

        logging.debug("Connection successful")

    def data_received(self, data: bytes, datatype: asyncssh.DataType) -> None:
        """New data coming in"""

        logging.debug(f"Received data: {data}")
        self._dispatch(data)

    def eof_received(self) -> None:
        """Got an EOF, close the channel"""

        logging.debug("EOF")
        self._chan.exit(0)

    def _dispatch(self, data: bytes) -> None:
        try:
            request = json.loads(gzip.decompress(data).decode('utf-8'))

            if 'id' not in request:
                logging.info("Malformed request: missing 'id'")
                self._send_response(0, 400, {"message": "Missing 'id'"})

            if 'request_type' not in request:
                logging.info("Malformed request: missing 'request_type'")
                self._send_response(request['id'], 400, {"message": "Missing 'request_type'"})

            if 'target_resource' not in request:
                logging.info("Malformed request: missing 'target_resource'")
                self._send_response(request['id'], 400, {"message": "Missing 'target_resource'"})

            if 'router' not in request:
                logging.info("Malformed request: missing 'router'")
                self._send_response(request['id'], 400, {"message": "Missing 'router'"})

            if request['request_type'] == 'POST' and 'data' not in request['request']:
                logging.info("Malformed request: missing 'data'")
                self._send_response(request['id'], 400, {"message": "Missing 'data'"})

            elif request['request_type'] == 'UPDATE' and 'data' not in request['request']:
                logging.info("Malformed request: missing 'data'")
                self._send_response(request['id'], 400, {"message": "Missing 'data'"})

            loop = asyncio.get_event_loop()

            if request['request_type'] in self.stream_types:
                asyncio.run_coroutine_threadsafe(self.__process_stream(request), loop)
                return None

            asyncio.run_coroutine_threadsafe(self.__process_request(request), loop)
            return None

        except Exception as exc:
            logging.info(f"Unable to process request: {exc}")
            self._send_response(0, 400, {"message": "Unable to process request"})
            return None

    async def __process_request(self, request: MutableMapping) -> None:
        if request['request_type'] not in self._callbacks:
            logging.info(f"No callback found for {request['request_type']}")
            self._send_response(request['id'], 404)
            return None

        if request['router'] not in self._callbacks[request['request_type']]:
            logging.info(f"No callback found for {request['request_type']} on {request['router']}")
            self._send_response(request['id'], 404)
            return None

        callback = self._callbacks[request['request_type']][request['router']]

        prepared_request = {
            'target_resource': request['target_resource'],
            'data': request['data']
        }

        try:
            response = await callback(**prepared_request)
            self._send_response(
                request_id=request['id'],
                ssh_response_code=200,
                response=response
            )

        except Exception as exc:
            logging.info(f"Internal error when executing {request['request_type']} on {request['resource']}")
            self._send_response(request['id'], 500, {"message": str(exc), "traceback": traceback.format_exc()})
            return None

    async def __process_stream(self, request: MutableMapping) -> None:
        if request['request_type'] not in self._callbacks:
            logging.info(f"No request type found for {request['request_type']}")
            self._send_response(request['id'], 404)
            return

        if request['router'] not in self._callbacks[request['request_type']]:
            logging.info(f"No router found for {request['request_type']} on {request['router']}")
            self._send_response(request['id'], 404)
            return

        callback = self._callbacks[request['request_type']][request['router']]

        prepared_request = {
            'target_resource': request['target_resource'],
            'data': request['data']
        }

        try:
            async for response in callback(**prepared_request):
                self._send_response(
                    request_id=request['id'],
                    ssh_response_code=200,
                    response=response
                )

        except Exception as exc:
            logging.info(f"Internal error when executing {request['request_type']} on {request['resource']}")
            self._send_response(request['id'], 500, {"message": str(exc), "traceback": traceback.format_exc()})

    def _send_response(
            self,
            request_id: float,
            ssh_response_code: int,
            response: Union[WSMessage, MutableMapping] = None
    ) -> None:
        """Send a response to the given client request"""

        ssh_response = {
            'id': str(uuid.uuid4()),
            'request_id': request_id,
            'ssh_response_code': ssh_response_code,
            'response': response
        }

        logging.info(f"{ssh_response_code} response to {request_id}")
        self._chan.write(gzip.compress(json.dumps(ssh_response, separators=(',', ':')).encode('utf-8')))
        return None