#!/usr/bin/env python3
from minitel.minitelhandler import MinitelHandler
from minitel.database import Migrate
import logging
import socketserver
from absl import flags, app


flags.DEFINE_string("address", "127.0.0.1", "Address to listen on")
flags.DEFINE_integer("port", 3615, "Port to listen on")



def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Starting, debug logging is enabled")
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    Migrate()
    listen = (flags.FLAGS.address, flags.FLAGS.port)
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
