import socketserver
import sys
import sys
import websockets
import asyncio
import time
from concurrent.futures import TimeoutError as ConnectionTimeoutError

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}/ws/status/") as ws:
        await ws.send(message)
        while(True):
            try:
                await asyncio.wait_for(ws.send('poll'), timeout=3)
                data = await asyncio.wait_for(ws.recv(), timeout=3)
                print(data)
                time.sleep(1)
            except Exception as e:
                print('Timed out. Trying again...')

if __name__ == "__main__":
    ip = ''
    port = 0
    for i, arg in enumerate(sys.argv):
        if i == 1:
            ip = arg
        elif i == 2:
            port = int(arg)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce(message = 'connected to progress server', host = ip, port = port))
