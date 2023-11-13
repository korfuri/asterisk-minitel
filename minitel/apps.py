import logging
import os
import pty
import minitel.tc as tc
from minitel.assets import asset
import pylev
import select
import subprocess


class BaseApp(object):
    nextApp = 'index'

    def __init__(self, m):
        self.m = m

    def begin(self):
        self.m.reset()

        def repeat():
            self.nextApp = type(self)
            return tc.Break
        self.m.keyHandlers[tc.kRepetition] = repeat


class ForkingApp(BaseApp):
    def spawn(self, cmd, env={}):
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
                              } | env) as process:
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
                        logging.debug("terminating the process")
                        process.kill()
                        _, _ = process.communicate()
            logging.debug("exited the process loop")
                        
    def handleCharacter(self, c):
        self._input = self._input + c

    def stopProcess(self):
        self._break = True
        return tc.Break

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
        apps_directory[name.lower().strip()] = cls
        if aliases is not None:
            for a in aliases:
                apps_directory[a.lower().strip()] = cls
        return cls
    return decorate


def appForCode(code):
    """Returns the app class corresponding to the given code.

    This is used by the 3615 app to get the next app to execute. This
    can also be invoked with code "index" to get back to the home
    page.

    If a class is passed, then return this as the next app. If a
    string is passed, do a best match using Levenshtein distance with
    a max distance of 2, which allows for some typos.
    """
    global apps_directory
    if type(code) == type:
        return code
    code = code.lower().strip()
    logging.info("Dispatching for %s", code)
    best = (999, None)
    for entry in apps_directory:
        d = pylev.levenshtein(entry, code)
        if d == 0:
            return apps_directory.get(code)
        if d < best[0]:
            best = d, entry
    if best[0] > 1:
        logging.info("Unknown code %s, known codes are: %s", code, apps_directory)
        code = "index"
    else:
        code = best[1]
    return apps_directory.get(code)


def reset_directory():
    global apps_directory
    apps_directory = {}
