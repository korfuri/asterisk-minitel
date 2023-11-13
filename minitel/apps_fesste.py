import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.database import GetEngine, QuestEntry


@register("fesste", ["index"])
class FessteHome(BaseApp):
    def getLeaderboard(self):
        with Session(GetEngine()) as session:
            stmt = select(QuestEntry.nick, func.count(QuestEntry.quest).label("count")).group_by(QuestEntry.nick).order_by(desc("count")).limit(9)
            return [(x.count, x.nick) for x in session.execute(stmt)]

    def interact(self):
        self.m.sendfile(asset("fesste/HOMEPAGE.vdt"))
        scores = self.getLeaderboard()
        for idx, (score, nick) in enumerate(scores):
            self.m.pos(16 + idx, 28)
            self.m._write(tc.tBgColor(tc.clMagenta))
            self.m.print('%02d' % score)
            self.m._write(tc.tBgColor(tc.clBlack))
            self.m.print(' %8s' % nick)
        code = self.m.addInputField(24, 2, 12, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        c = code.contents
        match c:
            case '1':
                c = 'regles'
            case '2':
                c = 'programme'
            case '3':
                c = 'annonces'
            case '4':
                c = 'horoscope'
        logging.debug("Code: %s", c)
        self.nextApp = appForCode(c)

@register("consentement")
class ConsentementApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("fesste/consentement.vdt"))
        self.m.handleInputsUntilBreak()
