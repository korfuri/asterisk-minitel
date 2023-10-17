import logging
import os
import pty
import tc
import select
import subprocess

class BaseApp(object):
    def __init__(self, m):
        self.m = m

    def begin(self):
        self.m.reset()

class ForkingApp(BaseApp):
    def spawn(self, cmd):
        self._input = bytes(0)
        self._break = False
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
            while process.poll() is None:
                rs, _, _ = select.select([master, self.m.socket], [], [])
                for r in rs:
                    if r is master:
                        data = os.read(master, 1000)
                        self.m._write(data)
                    else:
                        self.m.handleNextInput()
                        os.write(master, self._input)
                        self._input = bytes(0)
                        if self._break:
                            process.kill()
                            _, _ = process.communicate()

    def handleCharacter(self, c):
        self._input = self._input + c

    def stopProcess(self):
        self._break = True

    def begin(self):
        super().begin()
        self.m.keyHandlers[tc.kEnvoi] = self.stopProcess
        self.m.keyHandlers[tc.kRetour] = self.stopProcess
        self.m.keyHandlers[tc.kSommaire] = self.stopProcess
        self.m.keyHandlers[tc.kGuide] = self.stopProcess
        self.m.HandleCharacter = self.handleCharacter

apps_directory = {}

def register(name, aliases=None):
    global apps_directory
    def decorate(cls):
        apps_directory[name] = cls
        if aliases is not None:
            for a in aliases:
                apps_directory[a] = cls
        return cls
    return decorate

def appForCode(code):
    global apps_directory
    code = code.lower().strip()
    if code not in apps_directory:
        code = "index"
    return apps_directory.get(code)

@register("index", ["3615"])
class Index3615App(BaseApp):
    def interact(self):
        global apps_directory
        # self.m.sendfile("res/index3615.vtx")
        self.m.pos(1, 1)
        self.m.print("Code: .....................\r\n")
        for a in apps_directory:
            self.m.print("> %s\r\n" % a)
        code = self.m.addInputField(1, 7, 12, "", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        logging.debug("Code: %s", code.contents)
        self.nextApp = appForCode(code.contents)

BaseApp.nextApp = Index3615App
