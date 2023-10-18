import logging
import minitel.tc
import socketserver
from minitel.apps import appForCode

# Dummy imports to register application handlers
import minitel.apps_annuaire
import minitel.apps_forking
import minitel.apps_elections


class MinitelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Accepting a connection")
        m = minitel.tc.MinitelTerminal(self.request)
        try:
            m.start()
            m.reset()
            app = appForCode("index")
            while True:
                h = app(m)
                h.begin()
                h.interact()
                app = h.nextApp
        except minitel.tc.UserDisconnected:
            logging.info("User disconnected")
