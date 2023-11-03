import logging
import minitel.tc
import socketserver
from minitel.apps import appForCode

# Dummy imports to register application handlers
import minitel.apps_annonces
import minitel.apps_annuaire
import minitel.apps_elections
import minitel.apps_forking
import minitel.apps_quest
import minitel.apps_system


class MinitelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Accepting a connection")
        m = minitel.tc.MinitelTerminal(self.request)
        m.start()
        m.reset()
        app = appForCode("index")
        while True:
            try:
                h = app(m)
                h.begin()
                h.interact()
                app = h.nextApp
            except minitel.tc.UserDisconnected:
                logging.info("User disconnected")
                break
            except IOError as e:
                logging.info("Socket error: %s", e)
                break
            except Exception as e:
                logging.info("Triggered error page, error was: %s", e)
                app = appForCode("sys/error")
