from minitel.minitelhandler import MinitelHandler
import logging
import socketserver


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Starting")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", 3615), MinitelHandler) as server:
        logging.info("Listening on port 3615")
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
    main()
