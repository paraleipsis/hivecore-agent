import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

# URL = f'http://{HOST}:{PORT}/ws'
# URL = f'http://{HOST}:{PORT}/containers'
URL = f'http://{HOST}:{PORT}/containers/{"56957306c085"}'
# URL = f'http://{HOST}:{PORT}/containers/inspect'
# URL = f'http://{HOST}:{PORT}/containers/prune'


async def read_terminal(ws):
    while not ws.closed:
        await prompt_and_send(ws)


async def write_terminal(ws):
    while not ws.closed:
        msg = ws.receive()
        print(msg.data)


async def main():
    session = aiohttp.ClientSession()
    async with session as s:
        r = await s.get(URL)
    return await r.text()

    # async with session.ws_connect(URL) as ws:

        # asyncio.create_task(read_terminal(ws=ws))
        # asyncio.create_task(write_terminal(ws=ws))

        # await asyncio.gather(task1, task2)

        # async for msg in ws:
        #     print(msg.data)
            # await prompt_and_send(ws)



async def prompt_and_send(ws):
    new_msg_to_send = input()

    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print(asyncio.run(main()))