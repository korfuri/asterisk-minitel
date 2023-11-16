import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select
from sqlalchemy.orm import Session
from minitel.database import Classified, GetEngine


@register("annonces", ["ulla", "meetic"])
class AnnoncesApp(BaseApp):
    def getPage(self, page=0):
        with Session(GetEngine()) as session:
            stmt = select(Classified).order_by(Classified.id.desc()).offset(5*page).limit(5)
            return [x.contents for x in session.scalars(stmt)]

    def getPageCount(self):
        with Session(GetEngine()) as session:
            return session.query(Classified.id).count() / 5

    def nextPage(self):
        self.page = self.page + 1
        if self.page > self.getPageCount():
            self.page = 0
        self.showPage()
        return tc.Break

    def interact(self):
        self.page = 0
        self.m.keyHandlers[tc.kSuite] = self.nextPage
        self.m.keyHandlers[tc.kEnvoi] = self.compose
        self.showPage()

    def showPage(self):
        self.m.sendfile(asset("petitesannonces_header.vdt"))
        for i, a in enumerate(self.getPage(self.page)):
            self.m.textBox(line=5 + i * 4, col=2, width=38, height=3, text=a, effects=(tc.tFgColor(tc.clWhite) + tc.tBgColor(tc.clBlue)))
        pageStr = 'page %2d/%2d' % (self.page + 1, self.getPageCount() + 1)
        if len(pageStr) > 10:
            pageStr = 'page %3d' % (self.page + 1)
        if len(pageStr) > 10:
            pageStr = ''
        self.m.pos(2, 30)
        self.m.print(pageStr)
        self.m.handleInputsUntilBreak()

    def compose(self):
        self.m.sendfile(asset("petitesannonces_compose.vdt"))
        self.m.sendfile(asset("coeur.vdt"))
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        annonce = self.m.addInputField(7, 3, 36, "", lines=3)
        self.m.handleInputsUntilBreak()
        if self.m.lastControlKey() == tc.kEnvoi:
            data = annonce.contents.strip()
            if len(data) > 0:
                with Session(GetEngine()) as session:
                    session.add(Classified(contents=data))
                    session.commit()
            self.nextApp = AnnoncesApp
