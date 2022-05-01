import sys
import websockets
import asyncio

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await ws.send(message)
        await ws.recv()

if __name__ == "__main__":
    ip = ''
    port = 0
    for i, arg in enumerate(sys.argv):
        if i == 1:
            ip = arg
        elif i == 2:
            port = int(arg)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce(message = 'connected!', host = ip, port = port))
