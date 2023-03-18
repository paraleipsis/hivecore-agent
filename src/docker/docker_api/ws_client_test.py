import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

# URL = f'http://{HOST}:{PORT}/ws'
# URL = f'http://{HOST}:{PORT}/containers'
# URL = f'http://{HOST}:{PORT}/containers/{"56957306c085"}'
# URL = f'http://{HOST}:{PORT}/containers/inspect'
# URL = f'http://{HOST}:{PORT}/containers/prune'
# URL = f'http://{HOST}:{PORT}/containers/run'
# URL = f'http://{HOST}:{PORT}/containers/{"da47517af819"}/logs'
# URL = f'http://{HOST}:{PORT}/containers/{"3442403c99f2"}/terminal'
URL = f'http://{HOST}:{PORT}/containers/{"3442403c99f2"}/stats'


async def read_terminal(ws):
    while not ws.closed:
        await prompt_and_send(ws)


async def write_terminal(ws):
    while not ws.closed:
        msg = ws.receive()
        print(msg.data)


async def main():
    session = aiohttp.ClientSession()
    # params = {'name': 'nginx-test'}
    # data = {'Image': 'nginx', 'Volumes': ['/tmp', '/mnt']}
    # data = json.dumps(data)
    # async with session as s:
    #     r = await s.post(URL, params=params, data=data)
    # return await r.text()

    async with session.ws_connect(URL) as ws:
        # logs, stats test
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await callback(msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

        # terminal test
        # async for msg in ws:
        #     await prompt_and_send(ws)
        #     print(msg.data)


async def callback(msg):
    print(msg)


async def prompt_and_send(ws):
    new_msg_to_send = input()

    await ws.send_str(new_msg_to_send)

if __name__ == '__main__':
    print(asyncio.run(main()))
