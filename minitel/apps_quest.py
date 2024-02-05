from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from minitel.database import QuestEntry, GetEngine
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.ImageMinitel import ImageMinitel
from PIL import Image

# @register("sys/quests")
class QuestsSlideshowApp(BaseApp):
    def interact(self):
        basedir = "cliparts"
        files = os.listdir(asset(basedir))
        for f in files:
            logging.info("Next slide: %s", f)
            self.m.reset()

            self.m.pos(1, 1)
            self.m.setTextMode()
            self.m.print(' ' + f)

            image = Image.open(asset(basedir + "/" + f))
            image.thumbnail((80, 60), Image.LANCZOS)
            image_minitel = ImageMinitel()
            image_minitel.importer(image)
            image_minitel.envoyer(self.m, 1, 2)


            # self.m.sendfile(asset("quests/" + f))
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kSommaire:
                break

@register("legends", ["legendes"])
class LegendsApp(BaseApp):
    """A tribute to winners of previous quest games."""
    def interact(self):
        self.m.sendfile(asset("legends.vdt"))
        self.m.handleInputsUntilBreak()

@register("leaderboard")
class LeaderboardApp(BaseApp):
    def getLeaderboard(self):
        with Session(GetEngine()) as session:
            stmt = select(QuestEntry.nick, func.count(QuestEntry.quest).label("count")).group_by(QuestEntry.nick).order_by(desc("count")).limit(15)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def interact(self):
        self.m.sendfile(asset("leaderboard.vdt"))
        for i, l in enumerate(self.getLeaderboard(), start=1):
            self.m.pos(4 + i, 2)
            if i == 1:
                self.m.setInverse()
            self.m.print('%2d %10s %d' % (i, l[1], l[0]))
        self.m.handleInputsUntilBreak()


class BaseQuestApp(BaseApp):
    def show_asset(self):
        basedir = "cliparts"
        image = Image.open(asset("%s/%s.png" % (basedir, self.name)))
        image.thumbnail((80, 60), Image.LANCZOS)
        image_minitel = ImageMinitel()
        image_minitel.importer(image)
        image_minitel.envoyer(self.m, 1, 2)

    def interact(self):
        self.show_asset()

        self.m.pos(24, 1)
        self.m.print("Ton nom pour la gloire: ........ > ")
        self.m.setInverse()
        self.m.print("ENVOI")
        nick = self.m.addInputField(24, 24, 8, "")

        def do_save():
            q = QuestEntry(nick=nick.contents.strip().upper(), quest=self.name)
            logging.debug("Saving quest record %s", q)
            try:
                with Session(GetEngine()) as session:
                    session.add(q)
                    session.commit()
                    self.nextApp = appForCode("index")  # Should this be a confirmation screen?
            except:
                self.nextApp = appForCode("index")  # This happens when someone tries to submit twice. Fun error page instead?
            return tc.Break

        self.m.keyHandlers[tc.kEnvoi] = do_save
        self.m.handleInputsUntilBreak()


class ObsoleteQuestApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("quests/%s.vdt" % self.name))
        self.m.pos(24, 1)
        self.m.print("Tu as gagné 0 point(s). Retour: SOMMAIRE")
        self.m.handleInputsUntilBreak()

def make_quests():
    # Obsolete quests
    for kw in ["ADN",
               "ANTIQUE",
               "AVENTURES",
               "BROUETTE",
               "BUNNY",
               "CBT",
               "CERCLE",
               "DEPRIME",
               "FACIAL",
               "GALOP",
               "LGBT",
               "MANET",
               "MARLBORO",
               "PIAGGIO",
               "RETRAITE",
               "SPACE",
               "TAMBOUR",
               "TIMBRE",
               "TIMY",
               "VITESSE",
               "CHATPSYCHE",
               "DEFONCE",
               "DISCO",
               "RADIO",
               ]:
        class foo(ObsoleteQuestApp):
            name = kw
        register(kw)(foo)

    for kw in [
            'ANTITABAC',
            'AQUARIUM',
            'ATHENES',
            'AWOO',
            'BEBEBOULE',
            'BOBBRICO',
            'BONPOINT',
            'BOOOOOO',
            'BOWLING',
            'CADEAU',
            'CAMION',
            'CANADA',
            'CANDYCANE',
            'CARMEN',
            'CERISE',
            'CHAMPIS',
            'BONAP',
            'SMOKEY',
            'CHIENCOOL',
            'CLOCHES',
            'COWBOY',
            'CRABE',
            'CRANE',
            'CREAMPIE',
            'CUPCAKE',
            'DESSERT',
            'ENQUETE',
            'ETIRE',
            'F1',
            'FERME',
            'FIANCE',
            'FIXIT',
            'FOOT',
            'FROMAGE',
            'FUZZYLOVE',
            'GOLF',
            'GROSNERD',
            'HALLOWEEN',
            'HAMSTER',
            'HELICO',
            'HOSTO',
            'ILOVEYOU',
            'IRLANDE',
            'KARAOKE',
            'LAMPEGENIE',
            'MABITE',
            'MMESOLEIL',
            'MADMAX',
            'MAGICIEN',
            'MAIS',
            'MECANO',
            'MEDEVAC',
            'MULTIMEDIA',
            'NOEL',
            'OEUFS',
            'ORAGE',
            'PASTEK',
            'PILOTE',
            'PIQUANT',
            'PIRATE',
            'PLOMBERIE',
            'RUNWAY',
            'SPACEJAM',
            'SYDNEY',
            'TENNIS',
            'TI82',
            'TITANIC',
            'TORTUE',
            'TRESOR',
            'TREX',
            'TSOINSTOIN',
            'VALISE',
            'WATW',
    ]:
        class foo(BaseQuestApp):
            name = kw
        register(kw)(foo)

make_quests()
