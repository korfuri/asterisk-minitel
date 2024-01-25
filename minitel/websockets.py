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
            raise IOError from e

    def recv(self, maxlen=1):
        """Read from the websocket.

        If more than `maxlen` bytes are available to read (or are
        already in the read buffer), store the remainder in the read
        buffer. Only actually read from the websocket when the read
        buffer is empty, i.e. make no attempt to read exactly `maxlen`
        bytes.
        """
        try:
            if len(self.buffer) > 0:
                data, self.buffer = self.buffer[:maxlen], self.buffer[maxlen:]
            else:
                data = self.ws.recv()
                data, self.buffer = data[:maxlen], data[maxlen:]
            return data.encode()
        except websockets.exceptions.ConnectionClosed as e:
            raise IOError from e


def handler(ws):
    mh = WebsocketHandler(SocketAdapter(ws))
    mh.handle()

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
