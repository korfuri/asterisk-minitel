import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode


@register("annonces", ["ulla", "meetic"])
class AnnoncesApp(BaseApp):
    def interact(self):
        self.m.sendfile("assets/petitesannonces_header.vdt")

        # 1 classified 
        self.m.handleInputsUntilBreak()
