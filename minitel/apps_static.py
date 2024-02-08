import datetime
import logging
import minitel.tc as tc
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

@register("giscorp")
class GiscorpApp(StaticApp):
    def get_slides(self):
        return [asset("fesste/giscorp_%d.vdt") % x for x in range(10)]

@register("jeu", ["jeux", "rocher", "roche", "rochers", "roches"])
class JeuRochersApp(StaticApp):
    def get_slides(self):
        return [asset("fesste/jeu_%d.vdt") % x for x in range(4)]

@register("lineup", ["dj", "djs", "music", "musique", "line up"])
class JeuRochersApp(StaticApp):
    def get_slides(self):
        return [asset("fesste/dj-%s.vdt") % x for x in ["vendredi", "samedi", "dimanche"]]

    def get_start_idx(self):
        now = datetime.datetime.now()
        if now < datetime.datetime(2024, 2, 10, 8, 0):  # 08AM samedi
            return 0
        elif now > datetime.datetime(2024, 2, 11, 8, 0):  # 08AM dimanche
            return 2
        else:
            return 1
