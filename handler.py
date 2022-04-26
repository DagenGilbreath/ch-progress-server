import socketserver
import sys

class MyTCPHandler(socketserver.StreamRequestHandler):
    def __init__(self, ip, port, server_id):
        self.ip = ip
        self.port = port
        self.id = server_id
        self.open = True
    
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

if __name__ == "__main__":
    ip = ''
    port = 0
    for i, arg in enumerate(sys.argv):
        if i == 1:
            ip = arg
        elif i == 2:
            port = int(arg)
        elif i == 3:
            AWS_ACCESS_KEY = arg
        elif i == 4:
            AWS_SECRET_ACCESS_KEY = arg

    aServer = socketserver.TCPServer((ip, port), MyTCPHandler)

    # Listen forever
    aServer.serve_forever()