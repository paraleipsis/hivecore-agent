import asyncio

from aiodocker import Docker

from docker.docker_api import containers

import aiohttp.web


async def read_terminal(terminal_session, ws):
    while not ws.closed:
        output = await terminal_session.read_out()
        await ws.send_str(str(output.data, encoding='utf8'))


async def write_terminal(terminal_session, ws):
    async for msg in ws:
        cmd = bytes(msg.data + '\r\n', encoding='utf8')
        await terminal_session.write_in(cmd)


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')
    async with Docker() as session:
        terminal_session = await containers.container_terminal(docker_session=session, container_id='57')
        async with terminal_session as terminal:

            task1 = asyncio.create_task(read_terminal(terminal_session=terminal, ws=ws))
            task2 = asyncio.create_task(write_terminal(terminal_session=terminal, ws=ws))

            await asyncio.gather(task1, task2)

            # async for msg in ws:
            #     cmd = bytes(msg.data + '\r\n', encoding='utf8')
            #     await terminal.write_in(cmd)
            #     output = await terminal.read_out()
            #     await ws.send_str(str(output.data, encoding='utf8'))


    print('Websocket connection closed')
    return ws


def main():
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.get('/ws', websocket_handler)])
    aiohttp.web.run_app(app)


if __name__ == '__main__':
    main()
