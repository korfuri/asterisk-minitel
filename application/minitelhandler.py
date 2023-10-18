import logging
import tc
import socketserver
from apps import appForCode

# Dummy imports to register application handlers
import apps_annuaire
import apps_forking
import apps_elections


class MinitelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Accepting a connection")
        m = tc.MinitelTerminal(self.request)
        try:
            m.start()
            m.reset()
            app = appForCode("index")
            while True:
                h = app(m)
                h.begin()
                h.interact()
                app = h.nextApp
        except tc.UserDisconnected:
            logging.info("User disconnected")
