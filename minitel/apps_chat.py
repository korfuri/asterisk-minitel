import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
from sqlalchemy import select
from sqlalchemy.orm import Session
from minitel.database import ChatMessage, GetEngine


@register("chat")
class ChatApp(BaseApp):
    def interact(self):
        self.nick = ''
        self.channel = ''
        while not self.ready():
            self.m.sendfile(asset("chat_welcome.vdt"))
            # channel = self.m.addInputField(11, 20, 1, self.channel)
            nick = self.m.addInputField(15, 11, 8, self.nick)
            self.m.keyHandlers[tc.kEnvoi] = tc.Break
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kEnvoi:
                self.nick = nick.contents.strip().upper()
                self.channel = '1'
            elif self.m.lastControlKey() in (tc.kSommaire, tc.kRetour):
                break
        if self.ready():
            self.chat()
        
    def ready(self):
        return len(self.nick) > 0 and self.channel in ('1', '2')
                
    def getMessages(self):
        with Session(GetEngine()) as session:
            stmt = select(ChatMessage).where(ChatMessage.channel == self.channel).order_by(ChatMessage.id.desc()).limit(20)
            return [{'nick': x.nick, 'message': x.message} for x in session.scalars(stmt)]

    def refresh(self):
        messages = self.getMessages()
        messages.reverse()
        self.m.sendfile(asset("chat_chat.vdt"))
        self.m.pos(3, 1)
        for m in messages:
            self.m.print("%s> %s%s" % (m['nick'], m['message'], '\r\n' if len(m['message']) < 30 else ''))

    def chat(self):
        self.refresh()
        msg = self.m.addInputField(23, 6, 29, "")
        def post_msg():
            m = msg.contents.strip()
            if len(m) == 0:
                return
            with Session(GetEngine()) as session:
                session.add(ChatMessage(nick = self.nick,
                                        channel = self.channel,
                                        message = m))
                session.commit()
            msg.contents = ''
            self.refresh()
            self.m._write(msg.display())
        def refresh():
            self.refresh()
            self.m._write(msg.display())
        self.m.keyHandlers[tc.kEnvoi] = post_msg
        self.m.keyHandlers[tc.kRepetition] = refresh
        self.m.keyHandlers[tc.kSuite] = refresh
        self.m.handleInputsUntilBreak()
