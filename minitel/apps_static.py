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
class ChateauPSlidesApp(StaticApp):
    def get_slides(self):
        return [asset("chateaup/%s") % x for x in os.listdir(asset("chateaup"))]

class ChateauPWikiAeriens(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_AER_%dsur3.vdt") % x for x in range(1, 4)]

class ChateauPWikiLCTA(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_LCTA_%dsur2.vdt") % x for x in range(1, 3)]

class ChateauPWikiMini(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_Mini_%dsur2.vdt") % x for x in range(1, 3)]

class ChateauPWikiPlanete(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_PLANETE_1sur1.vdt")]

class ChateauPWikiResi(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_RESI_1sur1.vdt")]

class ChateauPWikiCOM(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_COM_%dsur2.vdt") % x for x in range(1, 3)]

class ChateauPWikiROE(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_ROE_1sur1.vdt")]

class ChateauPWikiPEZ(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_PEZ_1sur1.vdt")]

class ChateauPWikiOEU(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_OEU_%dsur2.vdt") % x for x in range(1, 3)]

class ChateauPWikiTIT(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_TIT_1sur1.vdt")]

class ChateauPWikiBEN(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_BEN_1sur1.vdt")]

class ChateauPWikiLAP(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_LAP_1sur1.vdt")]

class ChateauPWikiALC(StaticApp):
    def get_slides(self):
        return [asset("chateaup/Wiki_ALC_1sur1.vdt")]
