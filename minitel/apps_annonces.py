import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from sqlalchemy import select
from sqlalchemy.orm import Session
from minitel.database import Classified, GetEngine


@register("annonces", ["ulla", "meetic"])
class AnnoncesApp(BaseApp):
    def getPage(self, page=0):
        with Session(GetEngine()) as session:
            stmt = select(Classified).order_by(Classified.id.desc()).offset(5*page).limit(5)
            return [x.contents for x in session.scalars(stmt)]

    def nextPage(self):
        self.page = self.page + 1
        self.showPage()
        return tc.Break

    def populateDummyData(self):  # TODO remove me
        with Session(GetEngine()) as session:
            objs = [Classified(contents=x) for x in [
                "Si tu aimes les mecs chauds appelle moi au 45 24 7000",
                "JH cherche F ou cpl dans le 75",
                "je vends une mob peugeot, contactez la boulangerie Sanzot si interesse",
            ]]
            session.add_all(objs)
            session.commit()

    def interact(self):
        self.page = 0
        self.m.keyHandlers[tc.kSuite] = self.nextPage
        self.m.keyHandlers[tc.kEnvoi] = self.compose
        self.showPage()

    def showPage(self):
        self.m.sendfile("assets/petitesannonces_header.vdt")
        for i, a in enumerate(self.getPage(self.page)):
            self.m.textBox(line=5 + i * 4, col=2, width=38, height=3, text=a, effects=(tc.tFgColor(tc.clWhite) + tc.tBgColor(tc.clBlue)))
        self.m.handleInputsUntilBreak()

    def compose(self):
        self.m.sendfile("assets/petitesannonces_compose.vdt")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        annonce = self.m.addInputField(7, 2, 37, "")
        self.m.handleInputsUntilBreak()
        if self.m.lastControlKey() == tc.kEnvoi:
            data = annonce.contents.strip()
            if len(data) > 0:
                with Session(GetEngine()) as session:
                    session.add(Classified(contents=data))
                    session.commit()
            self.nextApp = AnnoncesApp