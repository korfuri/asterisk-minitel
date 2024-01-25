import importlib
import logging
import minitel.tc as tc
import socketserver
from minitel.apps import appForCode
import time
import traceback


import minitel.all_apps

class MinitelHandler(object):
    def handle(self):
        logging.info("Accepting a connection from %s" % self.get_origin())
        m = tc.MinitelTerminal(self.get_socket())
        self.wait_terminal_ready(m)
        m.reset()
        app = appForCode("index")
        while True:
            try:
                h = app(m)
                h.begin()
                h.interact()
                app = appForCode(h.nextApp)
            except tc.UserDisconnected:
                logging.info("User disconnected, %s", traceback.format_exc())
                break
            except IOError:
                logging.info("Socket error: %s", traceback.format_exc())
                break
            except Exception:
                logging.info("Triggered error page, error was: %s", traceback.format_exc())
                app = appForCode("sys/error")


class WebsocketHandler(MinitelHandler):
    def __init__(self, socket):
        self.socket = socket

    def get_socket(self):
        return self.socket

    def get_origin(self):
        return "WebSocket"

    def wait_terminal_ready(self, m):
        m.query_capabilities()


class TCPHandler(MinitelHandler, socketserver.BaseRequestHandler):
    def get_socket(self):
        return self.request

    def get_origin(self):
        return "TCP"

    def wait_terminal_ready(self, m):
        m.start()
