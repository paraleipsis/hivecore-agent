import threading
import asyncio

class TerminalStream():
    def __init__(self, websocket, terminal_socket):
        super(TerminalStream, self).__init__()
        self.websocket = websocket
        self.terminal_socket = terminal_socket

    async def terminal(self):
        while self.websocket:
            try:
                dockerStreamStdout =  self.terminal_socket.recv(2048)
                if dockerStreamStdout is not None:
                    await self.websocket.send(str(dockerStreamStdout, encoding='utf-8'))
                else:
                    print("docker daemon socket is close")
                    await self.websocket.close()
            except Exception as e:
                print(f"docker daemon socket err: {e}")
                await self.websocket.close()

    async def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.terminal)
        loop.close()
