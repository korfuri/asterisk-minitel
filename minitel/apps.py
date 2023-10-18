import logging
import os
import pty
import minitel.tc as tc
import select
import subprocess


class BaseApp(object):
    def __init__(self, m):
        self.m = m

    def begin(self):
        self.m.reset()

        def repeat():
            self.nextApp = type(self)
            return tc.Break
        self.m.keyHandlers[tc.kRepetition] = repeat


class ForkingApp(BaseApp):
    def spawn(self, cmd):
        self._input = bytes(0)
        self._break = False
        (master, slave) = pty.openpty()
        with subprocess.Popen(cmd,
                              stdin=slave,
                              stdout=slave,
                              stderr=slave,
                              close_fds=True,
                              shell=True,
                              env={
                                  "PATH": os.getenv("PATH"),
                                  "TERM": self.m.terminfo,
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
    """Registers an App to the main directory.

    Users can then call this app by name from the 3615 home.

    """
    global apps_directory

    def decorate(cls):
        assert(isinstance(cls, type))
        apps_directory[name] = cls
        if aliases is not None:
            for a in aliases:
                apps_directory[a] = cls
        return cls
    return decorate


def appForCode(code):
    """Returns the app class corresponding to the given code.

    This is used by the 3615 app to get the next app to execute. This
    can also be invoked with code "index" to get back to the home
    page.

    """
    global apps_directory
    code = code.lower().strip()
    logging.info("Dispatching for %s", code)
    if code not in apps_directory:
        code = "index"
    return apps_directory.get(code)


@register("index", ["3615"])
class Index3615App(BaseApp):
    def interact(self):
        global apps_directory
        self.m.sendfile("assets/3615.vdt")
        code = self.m.addInputField(4, 9, 12, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        logging.debug("Code: %s", code.contents)
        self.nextApp = appForCode(code.contents)

BaseApp.nextApp = Index3615App
