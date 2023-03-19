import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

# URL = f'http://{HOST}:{PORT}/ws'
# URL = f'http://{HOST}:{PORT}/containers'
# URL = f'http://{HOST}:{PORT}/containers/{"56956c085"}'
# URL = f'http://{HOST}:{PORT}/containers/inspect'
# URL = f'http://{HOST}:{PORT}/containers/prune'
# URL = f'http://{HOST}:{PORT}/containers/run'
# URL = f'http://{HOST}:{PORT}/containers/{"da47517af819"}/logs'
# URL = f'http://{HOST}:{PORT}/containers/{"3442403c99f2"}/terminal'
# URL = f'http://{HOST}:{PORT}/containers/{"3442403c99f2"}/stats'
# URL = f'http://{HOST}:{PORT}/images/build'
# URL = f'http://{HOST}:{PORT}/system/events'
URL = f'http://{HOST}:{PORT}/system'


async def read_terminal(ws):
    while not ws.closed:
        await prompt_and_send(ws)


async def write_terminal(ws):
    while not ws.closed:
        msg = ws.receive()
        print(msg.data)

import json
async def main():
    session = aiohttp.ClientSession()
    # dockerfile = '''
    # # Shared Volume
    # FROM busybox:buildroot-2014.02
    # VOLUME /data
    # CMD ["/bin/sh"]
    # '''
    #
    # # params = {'name': 'nginx-test'}
    # data = {'fileobj': dockerfile, 'encoding': 'utf-8'}
    # data = json.dumps(data)
    async with session as s:
        r = await s.get(URL)
    return await r.text()

    # async with session.ws_connect(URL) as ws:
    #     # logs, stats test
    #     async for msg in ws:
    #         if msg.type == aiohttp.WSMsgType.TEXT:
    #             await callback(msg.data)
    #         elif msg.type == aiohttp.WSMsgType.CLOSED:
    #             break
    #         elif msg.type == aiohttp.WSMsgType.ERROR:
    #             break

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
