import logging
import minitel.tc as tc
import socketserver
from minitel.apps import appForCode
from absl import flags
import websockets

flags.DEFINE_bool("debug_reload_apps", False, "Debug only: reload apps dynamically on each interaction")

import minitel.all_apps


class MinitelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Accepting a connection")
        m = tc.MinitelTerminal(self.request)
        m.start()
        m.reset()
        app = appForCode("index")
        while True:
            if flags.FLAGS.debug_reload_apps:
                import minitel.all_apps
            try:
                h = app(m)
                h.begin()
                h.interact()
                app = appForCode(h.nextApp)
            except tc.UserDisconnected:
                logging.info("User disconnected")
                break
            except IOError as e:
                logging.info("Socket error: %s", e)
                break
            except Exception as e:
                logging.info("Triggered error page, error was: %s", e)
                app = appForCode("sys/error")


class WebsocketHandler():
    def handle(self, socket):
        logging.info("Accepting a websocket connection")
        m = tc.MinitelTerminal(socket)
        m.query_capabilities()
        m.reset()
        app = appForCode("index")
        while True:
            if flags.FLAGS.debug_reload_apps:
                import minitel.all_apps
            try:
                h = app(m)
                h.begin()
                h.interact()
                app = appForCode(h.nextApp)
            except tc.UserDisconnected:
                logging.info("User disconnected")
                break
            except IOError as e:
                logging.info("Socket error: %s", e)
                break
            except websockets.exceptions.ConnectionClosed as e:
                logging.info("Websocket closed: %s", e)
                break
            except Exception as e:
                logging.info("Triggered error page, error was: %s", e)
                app = appForCode("sys/error")
