#!/usr/bin/env python3
from minitel.minitelhandler import MinitelHandler
from minitel.database import Migrate
from minitel.websockets import startWebsocketHandler
from minitel.web import startWebServer
import logging
import socketserver
import threading
from absl import flags, app


flags.DEFINE_string("tty_address", "127.0.0.1", "Address to listen on for the tty server")
flags.DEFINE_integer("tty_port", 3615, "Port to listen on for the tty server")
flags.DEFINE_string("web_address", "127.0.0.1", "Address to listen on for the Web server")
flags.DEFINE_integer("web_port", None, "Port to listen on for the Web server")
flags.DEFINE_string("ws_address", "127.0.0.1", "Address to listen on for the WebSocket server")
flags.DEFINE_integer("ws_port", None, "Port to listen on for the WebSocket server")


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting, debug logging is enabled")
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    Migrate()
    if flags.FLAGS.ws_port is not None:
        ws_thread = threading.Thread(target=startWebsocketHandler,
                                     args=((flags.FLAGS.ws_address,
                                            flags.FLAGS.ws_port)))
        ws_thread.start()
    if flags.FLAGS.web_port is not None:
        web_thread = threading.Thread(target=startWebServer,
                                     args=((flags.FLAGS.web_address,
                                            flags.FLAGS.web_port)),)
        web_thread.start()
    
    listen = (flags.FLAGS.tty_address, flags.FLAGS.tty_port)
    with socketserver.ThreadingTCPServer(listen, MinitelHandler) as server:
        logging.info("Listening on %s:%s", *listen)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Interrupted manually")
            server.shutdown()
        except Exception as e:
            logging.warning("Terminating on uncaught exception: ", e)
            server.shutdown()
        logging.info("Exited cleanly")

if __name__ == "__main__":
    app.run(main)
