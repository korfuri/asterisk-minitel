import logging
import tc
import socketserver

class HelpApp:
    pass

apps_directory = {
    "help": HelpApp
}

class BaseApp(object):
    def __init__(self, m):
        self.m = m

    def begin(self):
        self.m.reset()

class Index3615App(BaseApp):
    def interact(self):
        # self.m.sendfile("res/index3615.vtx")
        self.m.pos(1, 1)
        self.m.print("Code: .....................")
        code = self.m.addInputField(1, 7, 12, "", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputs()
        logging.debug("Code: %s", code.contents)
        if code.contents == "ANNU":
            self.nextApp = AnnuaireApp

BaseApp.nextApp = Index3615App

class AnnuaireApp(BaseApp):
    def interact(self):
        self.m.sendfile("assets/3611.vtx")
        quoi = self.m.addInputField(5, 13, 28, "Une pomme", tc.clWhite)
        ou = self.m.addInputField(10, 13, 28, "Un verger", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputs()
        logging.debug("Searching for %s in %s", quoi.contents, ou.contents)


class MinitelHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info("Accepting a connection")
        m = tc.MinitelTerminal(self.request)
        try:
            m.read_ulm_header()
            m.reset()
            app = Index3615App
            while True:
                h = app(m)
                h.begin()
                h.interact()
                app = h.nextApp
        except tc.UserDisconnected:
            logging.info("User disconnected")
