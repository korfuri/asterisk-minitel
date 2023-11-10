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
        try:
            if data.find(b'\xff') > 0:
                data = data[:data.find(b'\xff')-1]
            d = data.decode()
            self.ws.send(d)
            return len(d)
        except websockets.exceptions.ConnectionClosed as e:
            raise IOError(e)

    def recv(self, maxlen=1):
        try:
            if len(self.buffer) < maxlen:
                data = self.ws.recv()
                self.buffer = self.buffer + data
            if len(self.buffer) >= maxlen:
                data = self.buffer[:maxlen]
                self.buffer = self.buffer[maxlen:]
            else:
                data = ''
            return data.encode()
        except websockets.exceptions.ConnectionClosed as e:
            raise IOError(e)


def handler(ws):
    mh = WebsocketHandler()
    mh.handle(SocketAdapter(ws))

def startWebsocketHandler(*listener):
    with websockets.sync.server.serve(handler, *listener) as server:
        logging.info("Websockets listening on ws://%s:%s", *listener)
        server.serve_forever()


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting, debug logging is enabled")
    Migrate()
    startWebsocketHandler()


if __name__ == '__main__':
    app.run(main)
