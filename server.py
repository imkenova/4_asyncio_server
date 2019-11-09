import asyncio

HOST = 'localhost'
PORT = 9090


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    print(data.decode())
    writer.write(data)
    await writer.drain()

    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, HOST, PORT, loop=loop)
server = loop.run_until_complete(coro)


print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass


server.close()
loop.run_until_complete(server.wait_closed())

loop.close()
