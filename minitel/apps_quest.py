from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from minitel.database import QuestEntry, QuestOwnership, GetEngine
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.ImageMinitel import ImageMinitel
from PIL import Image

# @register("a")
class QuestsSlideshowApp(BaseApp):
    def interact(self):
        basedir = "cliparts2"
        files = os.listdir(asset(basedir))
        files = sorted(files)
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
            try:
                pass
            except:
                self.m.pos(2,2)
                self.m.print("ERROR")

            # self.m.sendfile(asset("quests/" + f))
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kSommaire:
                break

# @register("legends", ["legendes"])
class LegendsApp(BaseApp):
    """A tribute to winners of previous quest games."""
    def interact(self):
        self.m.sendfile(asset("legends.vdt"))
        self.m.handleInputsUntilBreak()

@register("leaderboard")
class LeaderboardApp(BaseApp):
    def getLeaderboardVisitors(self):
        with Session(GetEngine()) as session:
            stmt = select(QuestEntry.nick, func.count(QuestEntry.quest).label("count")).group_by(QuestEntry.nick).order_by(desc("count")).limit(15)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def getLeaderboardVisited(self):
        with Session(GetEngine()) as session:
            subq = select(QuestEntry.quest, func.count(QuestEntry.nick).label("count")).group_by(QuestEntry.quest).subquery()
            stmt = select(QuestOwnership.nick, func.sum(subq.c.count).label("count")).join(subq, QuestOwnership.quest == subq.c.quest).where(QuestOwnership.nick != QuestEntry.nick).group_by(QuestOwnership.nick).order_by(desc("count")).limit(15)
            logging.debug(stmt)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def interact(self):
        self.m.sendfile(asset("leaderboard_toponly.vdt"))
        for i, l in enumerate(self.getLeaderboardVisitors(), start=1):
            self.m.pos(4 + i, 2)
            if i == 1:
                self.m.setInverse()
            self.m.print('%2d %10s       %d' % (i, l[1], l[0]))
        # for i, l in enumerate(self.getLeaderboardVisited(), start=1):
        #     self.m.pos(4 + i, 22)
        #     if i == 1:
        #         self.m.setInverse()
        #     self.m.print('%2d %10s %d' % (i, l[1], l[0]))
        self.m.handleInputsUntilBreak()


class BaseQuestApp(BaseApp):
    def show_asset(self):
        basedir = "cliparts"
        image = Image.open(asset("%s/%s.png" % (basedir, self.name)))
        image.thumbnail((80, 60), Image.LANCZOS)
        image_minitel = ImageMinitel()
        image_minitel.importer(image)
        image_minitel.envoyer(self.m, 1, 2)

    def is_owned(self):
        with Session(GetEngine()) as session:
            qo = session.get(QuestOwnership, self.name)
            return qo is not None

    def interact(self):
        self.show_asset()

        is_owned = self.is_owned()

        # if quest is owned:
        self.m.pos(24, 1)
        if is_owned:
            self.m.print("Ton nom pour la gloire: ........ > ")
        else:
            self.m.print("Ce code appartient à:   ........ > ")
        self.m.setInverse()
        self.m.print("ENVOI")
        nick = self.m.addInputField(24, 24, 8, "")

        def do_save():
            n = nick.contents.strip().upper()
            if n == '':
                return tc.Break
            q = QuestEntry(nick=n, quest=self.name)
            logging.debug("Saving quest record %s", q)
            try:
                with Session(GetEngine()) as session:
                    session.add(q)
                    session.commit()
                    self.nextApp = appForCode("index")  # Should this be a confirmation screen?
            except:
                self.nextApp = appForCode("index")  # This happens when someone tries to submit twice. Fun error page instead?
            return tc.Break

        def do_own():
            n = nick.contents.strip().upper()
            if n == '':
                return tc.Break
            qo = QuestOwnership(nick=n, quest=self.name)
            try:
                with Session(GetEngine()) as session:
                    session.add(qo)
                    session.commit()
                return do_save()
            except:
                self.nextApp = appForCode("index")
            return tc.Break

        if is_owned:
            self.m.keyHandlers[tc.kEnvoi] = do_save
        else:
            self.m.keyHandlers[tc.kEnvoi] = do_own

        self.m.handleInputsUntilBreak()


class ObsoleteQuestApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("quests/%s.vdt" % self.name))
        self.m.pos(24, 1)
        self.m.print("Tu as gagné 0 point(s). Retour: SOMMAIRE")
        self.m.handleInputsUntilBreak()

class ObsoletePNGQuestApp(BaseApp):
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
            'ALLO',
	    'BOSS',
	    'CHANCE',
	    'DICKBUTT',
	    'ECUREUIL',
	    'FRIDAY',
	    'FRY',
	    'HENTAI',
	    'LOLOL',
	    'NOKIA',
	    'NYAN',
	    'ORLY',
	    'PEACH',
	    'PIGFLY',
	    'PIKACHU',
	    'POE',
	    'PRIDE',
	    'SRSLY',
	    'UNICORN',
    ]:
        class foo(ObsoletePNGQuestApp):
            name = kw
        register(kw)(foo)

make_quests()
