import logging
import os
import pty
import tc
import select
import socketserver
import subprocess

class HelpApp:
    pass

class BaseApp(object):
    def __init__(self, m):
        self.m = m

    def begin(self):
        self.m.reset()

class AnnuaireApp(BaseApp):
    def interact(self):
        self.m.sendfile("assets/3611.vtx")
        quoi = self.m.addInputField(5, 13, 28, "Une pomme", tc.clWhite)
        ou = self.m.addInputField(10, 13, 28, "Un verger", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputs()
        logging.debug("Searching for %s in %s", quoi.contents, ou.contents)

class ForkingApp(BaseApp):
    def spawn(self, cmd):
        (master,slave) = pty.openpty()
        with subprocess.Popen(cmd,
                              stdin=slave,
                              stdout=slave,
                              stderr=slave,
                              close_fds=True,
                              shell=True,
                              env={
                                  "PATH": os.getenv("PATH"),
                                  "TERM": "minitel",
                                  "LINES": "24",
                                  "COLUMNS": "40",
                              }) as process:
            while True:
                if process.poll():
                    break
                rs, _, _ = select.select([master, self.m.socket], [], [])
                for r in rs:  # TODO this works, but we should do something where we abstract the input field logic and this and route events to one or the other so we can still handle minitel keys
                    if r is master:
                        data = os.read(master, 1000)
                        self.m._write(data)
                    else:
                        data = self.m._read(1000)
                        os.write(master, data)

    def interact(self):
        self.spawn(["nethack"])

        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.keyHandlers[tc.kRetour] = tc.Break
        self.m.keyHandlers[tc.kSommaire] = tc.Break
        self.m.keyHandlers[tc.kGuide] = tc.Break
        self.m.handleInputs()

apps_directory = {
    "HELP": HelpApp,
    "ANNU": AnnuaireApp,
    "HELLO": ForkingApp,
}

class Index3615App(BaseApp):
    def interact(self):
        # self.m.sendfile("res/index3615.vtx")
        self.m.pos(1, 1)
        self.m.print("Code: .....................")
        code = self.m.addInputField(1, 7, 12, "", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputs()
        logging.debug("Code: %s", code.contents)
        if code.contents in apps_directory:
            self.nextApp = apps_directory[code.contents]

BaseApp.nextApp = Index3615App

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
