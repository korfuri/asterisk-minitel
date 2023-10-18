import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode


@register("annu", ["annuaire", "3611"])
class AnnuaireApp(BaseApp):
    def interact(self):
        self.m.sendfile("assets/3611.vdt")
        quoi = self.m.addInputField(5, 13, 28, "", tc.clWhite)
        ou = self.m.addInputField(10, 13, 28, "", tc.clWhite)

        def do_search():
            logging.debug("Searching for %s in %s", quoi.contents, ou.contents)
            return tc.Break
        self.m.keyHandlers[tc.kEnvoi] = do_search

        def do_sommaire():
            self.nextApp = appForCode("index")
            return tc.Break
        self.m.keyHandlers[tc.kSommaire] = do_sommaire
        self.m.keyHandlers[tc.kGuide] = do_sommaire

        self.m.handleInputsUntilBreak()
