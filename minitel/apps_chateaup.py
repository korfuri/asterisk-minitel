import logging
import minitel.tc as tc
import random
import datetime
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.database import GetEngine, QuestEntry


@register("index")
class ChateauPHome(BaseApp):
    def getLeaderboard(self):
        with Session(GetEngine()) as session:
            stmt = select(QuestEntry.nick, func.count(QuestEntry.quest).label("count")).group_by(QuestEntry.nick).order_by(desc("count")).limit(13)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def interact(self):
        self.m.sendfile(asset("chateaup/accueil.vdt"))
        for i, l in enumerate(self.getLeaderboard()):
            self.m.pos(12 + i, 26)
            self.m._write(tc.tBgColor(tc.clMagenta))
            self.m.print('%02d' % l[0])
            self.m._write(tc.tBgColor(tc.clBlack))
            self.m.print(' %s' % l[1])
        code = self.m.addInputField(24, 2, 15, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        def goGuide():
            code.contents = 'guide'
            return tc.Break
        self.m.keyHandlers[tc.kGuide] = goGuide
        self.m.handleInputsUntilBreak()
        c = code.contents
        match c:
            case '1':
                c = 'horoscope'
            case '2':
                c = 'chat'
            case '3':
                c = 'wiki'
        logging.debug("Code: %s", c)
        self.nextApp = appForCode(c)


@register("telephonemaison")
class ChateauPTelephoneMaison(BaseApp):
    def interact(self):
        self.m.sendfile(asset("chateaup/TELEPHONEMAISON.vdt"))
        self.m.handleInputsUntilBreak()

import minitel.apps_static

def returnToWiki(cls):
    """Patch a class so its nextApp is the wiki app."""
    class Patched(cls):
        def interact(self):
            v = super(Patched, self).interact()
            self.nextApp = appForCode("wiki")
            return v
    return Patched

@register("wiki", ["wikilcta"])
class ChateauPWikiApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("chateaup/Wiki_root.vdt"))
        page = self.m.addInputField(24, 2, 3, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        pn = page.contents.strip()
        match pn:
            case '':
                self.nextApp = appForCode("index")
            case '1':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiAeriens)
            case '2':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiMini)
            case '3':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiResi)
            case '4':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiLCTA)
            case '5':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiPlanete)
            case '6':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiCOM)
            case '7':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiROE)
            case '8':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiPEZ)
            case '9':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiOEU)
            case '10':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiTIT)
            case '11':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiBEN)
            case '12':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiLAP)
            case '13':
                self.nextApp = returnToWiki(minitel.apps_static.ChateauPWikiALC)
            case _:
                self.nextApp = ChateauPWikiApp
