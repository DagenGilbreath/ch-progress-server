import sys
import sys
import websockets
import asyncio
import time
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import socketserver
import threading

sessions = {}

class MyTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print("Recieved one request from {}".format(self.client_address[0]))
        msg = self.rfile.readline().strip().decode()
        print("Data Recieved from client is: {}".format(msg))
        sessions[msg.split(';')[2]] = msg

def run_socket_server():
        aServer = socketserver.TCPServer(('0.0.0.0', 8080), MyTCPRequestHandler)
        # Listen forever
        aServer.serve_forever()

async def produce(message: str, host: str, port: int) -> None:
    async with websockets.connect(f"ws://{host}:{port}/ws/status/") as ws:
        await ws.send(message)
        
        x = threading.Thread(target=run_socket_server)
        x.start()

        while(True):
            try:
                await asyncio.wait_for(ws.send('poll'), timeout=0.5)
                data = await asyncio.wait_for(ws.recv(), timeout=0.5)
                # If csrf token not present in sesssions, create it
                if(data.replace('"', '') not in sessions and len(data) > 15):
                    sessions[data.replace('"', '')] = '5;Connected to Progress Server;{}'.format(data.replace('"', ''))
                # If a csrf token, send back progress (sessions[token])
                if(len(data) > 15):
                    print(data)
                    await asyncio.wait_for(ws.send(sessions[data.replace('"', '')]), timeout=0.5)
                    response = await asyncio.wait_for(ws.recv(), timeout=0.5)
                    print('Response: {}'.format(response))
                time.sleep(0.05)
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
    while True:
        try:
            loop.run_until_complete(produce(message = 'connected to progress server', host = ip, port = port))
        except Exception as e:
            print("Failed to connect to website")
