import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import os


@register("annu", ["annuaire", "3611"])
class AnnuaireApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("3611.vdt"))
        ou = self.m.addInputField(10, 13, 28, "", tc.tFgColor(tc.clRed))
        quoi = self.m.addInputField(5, 13, 28, "")

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

@register("clubmed")
class ClubMedApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("clubmed.vdt"))
        self.m.handleInputsUntilBreak()

@register("slides")
class SlideshowApp(BaseApp):
    def interact(self):
        files = os.listdir(asset("slideshow"))
        for f in files:
            logging.info("Next slide: %s", f)
            self.m.sendfile(asset("slideshow/" + f))
            self.m.handleInputsUntilBreak()
