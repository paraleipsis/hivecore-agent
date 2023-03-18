from typing import List

from aiohttp.web_ws import WebSocketResponse


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocketResponse] = []

    async def connect(self, websocket: WebSocketResponse, request):
        await websocket.prepare(request)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocketResponse):
        self.active_connections.remove(websocket)
        await websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocketResponse):
        await websocket.send_str(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_str(message)
