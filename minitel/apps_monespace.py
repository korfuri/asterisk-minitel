import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select
from sqlalchemy.orm import Session
from minitel.database import Space, GetEngine, SECRET_MAXLEN


class ValueError(Exception):
    """Invalid data was entered in a users' profile."""
    def __init__(self):
        super().__init__("Invalid space data")


@register("monespace")
class MonEspaceApp(BaseApp):
    secret = ''

    def getProfileByNick(self, nick):
        if nick == '':
            raise ValueError()
        with Session(GetEngine()) as session:
            stmt = select(Space).where(Space.nick == nick)
            return session.scalars(stmt).first()

    def getProfileForSecret(self):
        if nick == '':
            raise ValueError()
        with Session(GetEngine()) as session:
            sp = session.get(Space, self.secret)
            return sp

    def setSecretFromNick(self, nick):
        sp = self.getProfileByNick(nick)
        self.secret = sp.secret

    def createProfile(self, nick):
        nick = nick.strip().upper()
        if nick == '':
            raise ValueError()
        with Session(GetEngine()) as session:
            sp = session.get(Space, self.secret)
            sp.nick = nick
            session.commit()

    def setProfileContents(self, contents):
        with Session(GetEngine()) as session:
            sp = session.get(Space, self.secret)
            if sp.nick == '':
                raise ValueError()
            sp.contents = contents
            session.commit()

    def addVisit(self):
        with Session(GetEngine()) as session:
            sp = session.get(Space, self.secret)
            sp.visits = sp.visits + 1
            session.commit()

    def interact(self):
        self.m.print("MonEspace\r\n")
        self.m.print("Qui voulez vous visiter? Ou GUIDE pour editer votre espace\r\n")
        self.m.print("....")
        def goGuide():
            self.m.print("Code?")
            code = self.m.addInputField(8, 1, SECRET_MAXLEN, "")
            self.m.handleInputsUntilBreak()
            self.m.print(code.contents)
        self.m.keyHandlers[tc.kGuide] = goGuide
        self.m.handleInputsUntilBreak()
