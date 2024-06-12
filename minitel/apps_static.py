import datetime
import logging
import minitel.tc as tc
import os
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset


class StaticApp(BaseApp):
    def get_start_idx(self):
        return 0

    def interact(self):
        slides = self.get_slides()
        idx = self.get_start_idx()
        while True:
            self.m.sendfile(slides[idx])

            self.m.pos(24, 10)
            if idx > 0:
                self.m.setInverse()
                self.m.print("RETOUR")
                self.m.setNotInverse()
            else:
                self.m.print("      ")
            self.m.print(" %d/%d " % ((idx + 1), len(slides)))
            if idx < len(slides) - 1:
                self.m.setInverse()
                self.m.print("SUITE")
                self.m.setNotInverse()

            self.m.pos(24, 29)
            self.m.print("Fin:")
            self.m.setInverse()
            self.m.print("SOMMAIRE")
            self.m.cursorOff()

            def prev():
                nonlocal idx
                idx = idx - 1
                if idx < 0:
                    idx = 0
                return tc.Break
            self.m.keyHandlers[tc.kRetour] = prev

            def next():
                nonlocal idx
                nonlocal slides
                idx = idx + 1
                if idx > len(slides) - 1:
                    idx = len(slides) - 1
                return tc.Break
            self.m.keyHandlers[tc.kSuite] = next
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kSommaire:
                break

@register("_slides")
class ChateauApp(StaticApp):
    def get_slides(self):
        return [asset("chateaup/%s") % x for x in os.listdir(asset("chateaup"))]
