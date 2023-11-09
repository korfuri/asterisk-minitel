import websockets
import websockets.sync.server
from minitel.minitelhandler import WebsocketHandler
from absl import app
from minitel.database import Migrate
import logging


class SocketAdapter(object):
    def __init__(self, websocket):
        self.ws = websocket
        self.buffer = ''

    def send(self, data):
        if data.find(b'\xff') > 0:
            data = data[:data.find(b'\xff')-1]
        d = data.decode()
        self.ws.send(d)
        return len(d)

    def recv(self, maxlen=1):
        if len(self.buffer) < maxlen:
            data = self.ws.recv()
            self.buffer = self.buffer + data
        if len(self.buffer) >= maxlen:
            data = self.buffer[:maxlen]
            self.buffer = self.buffer[maxlen:]
        else:
            data = ''
        return data.encode()


def handler(ws):
    mh = WebsocketHandler()
    mh.handle(SocketAdapter(ws))

def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting, debug logging is enabled")
    Migrate()
    # TODO ws_port flag
    with websockets.sync.server.serve(handler, 'localhost', 3611) as server:
        logging.info("Listening on ws://%s:%s", 'localhost', 3611)
        server.serve_forever()
    

if __name__ == '__main__':
    app.run(main)
