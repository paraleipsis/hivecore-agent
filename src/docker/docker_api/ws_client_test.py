import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

URL = f'http://{HOST}:{PORT}/ws'


async def read_terminal(ws):
    while not ws.closed:
        await prompt_and_send(ws)


async def write_terminal(ws):
    while not ws.closed:
        msg = ws.receive()
        print(msg.data)


async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:

        asyncio.create_task(read_terminal(ws=ws))
        asyncio.create_task(write_terminal(ws=ws))

        # await asyncio.gather(task1, task2)

        # async for msg in ws:
        #     print(msg.data)
            # await prompt_and_send(ws)



async def prompt_and_send(ws):
    new_msg_to_send = input()

    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())