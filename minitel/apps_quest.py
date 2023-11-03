from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from minitel.database import QuestEntry, GetEngine
import os
import logging
from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseQuestApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("quests/%s.vdt" % self.name))
        self.m.pos(24, 1)
        self.m.print("Ton nom pour la gloire: ........ > ")
        self.m._write(tc.tVideoInverseStart)
        self.m.print("ENVOI")
        nick = self.m.addInputField(24, 24, 8, "")

        def do_save():
            q = QuestEntry(nick=nick.contents.strip(), quest=self.name)
            logging.debug("Saving quest record %s", q)
            try:
                with Session(GetEngine()) as session:
                    session.add(q)
                    session.commit()
                    self.nextApp = appForCode("index")  # Should this be a confirmation screen?
            except:
                self.nextApp = appForCode("index")  # This happens when someone tries to submit twice. Fun error page instead?

        self.m.keyHandlers[tc.kEnvoi] = do_save
        self.m.handleInputsUntilBreak()


@register("sys/quests")
class QuestsSlideshowApp(BaseApp):
    def interact(self):
        files = os.listdir(asset("quests"))
        for f in files:
            logging.info("Next slide: %s", f)
            self.m.sendfile(asset("quests/" + f))
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kSommaire:
                break

# Todo: can i find a way to generate those iteratively?
# Wrapping the class declaration in a loop leads to re-declaration
# under the same name.
@register("ADN")
class ADN(BaseQuestApp):
    name = "ADN"

@register("ANTIQUE")
class ANTIQUE(BaseQuestApp):
    name = "ANTIQUE"

@register("AVENTURES")
class AVENTURES(BaseQuestApp):
    name = "AVENTURES"

@register("BROUETTE")
class BROUETTE(BaseQuestApp):
    name = "BROUETTE"

@register("BUNNY")
class BUNNY(BaseQuestApp):
    name = "BUNNY"

@register("CBT")
class CBT(BaseQuestApp):
    name = "CBT"

@register("CERCLE")
class CERCLE(BaseQuestApp):
    name = "CERCLE"

@register("DEPRIME")
class DEPRIME(BaseQuestApp):
    name = "DEPRIME"

@register("FACIAL")
class FACIAL(BaseQuestApp):
    name = "FACIAL"

@register("GALOP")
class GALOP(BaseQuestApp):
    name = "GALOP"

@register("LGBT")
class LGBT(BaseQuestApp):
    name = "LGBT"

@register("MANET")
class MANET(BaseQuestApp):
    name = "MANET"

@register("MARLBORO")
class MARLBORO(BaseQuestApp):
    name = "MARLBORO"

@register("PIAGGIO")
class PIAGGIO(BaseQuestApp):
    name = "PIAGGIO"

@register("RETRAITE")
class RETRAITE(BaseQuestApp):
    name = "RETRAITE"

@register("SPACE")
class SPACE(BaseQuestApp):
    name = "SPACE"

@register("TAMBOUR")
class TAMBOUR(BaseQuestApp):
    name = "TAMBOUR"

@register("TIMBRE")
class TIMBRE(BaseQuestApp):
    name = "TIMBRE"

@register("TIMY")
class TIMY(BaseQuestApp):
    name = "TIMY"

@register("VITESSE")
class VITESSE(BaseQuestApp):
    name = "VITESSE"
