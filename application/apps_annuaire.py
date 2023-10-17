import logging
import tc
from apps import BaseApp, register

@register("annu", ["annuaire", "3611"])
class AnnuaireApp(BaseApp):
    def interact(self):
        self.m.sendfile("assets/3611.vtx")
        quoi = self.m.addInputField(5, 13, 28, "Une pomme", tc.clWhite)
        ou = self.m.addInputField(10, 13, 28, "Un verger", tc.clWhite)
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        logging.debug("Searching for %s in %s", quoi.contents, ou.contents)
