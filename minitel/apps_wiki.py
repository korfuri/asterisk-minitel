from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from absl import flags
from minitel.database import GetEngine, WikiArticle, WIKI_TITLE_MAXLEN, normalize_wiki_title, QuestEntry
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
import re


@register("wiki", ["wikipocalypse"])
class WikiApp(BaseApp):
    wiki_re = re.compile("\[\[([^]]+)\]\]")

    def interact(self):
        self.nick = ''
        while not self.ready():
            self.m.sendfile(asset("wiki_welcome.vdt"))
            nick = self.m.addInputField(10, 11, 8, self.nick)
            self.m.keyHandlers[tc.kEnvoi] = tc.Break
            self.m.handleInputsUntilBreak()
            if self.m.lastControlKey() == tc.kEnvoi:
                self.nick = nick.contents.strip().upper()
            elif self.m.lastControlKey() in (tc.kSommaire, tc.kRetour):
                break
        if self.ready():
            return self.render_page("index")

    def ready(self):
        return len(self.nick) > 0
    
    def linkify(self, contents):
        """Returns a "linkified" page, i.e. a tuple of:

        - A bytes object that is the article'scontents ready to
          display with links underlined and indexed, e.g.

            bytes("The Minitel was a \x1b\x5avideotex\x1b\59[1]
            \x1b\x5aonline service\x1b\x59[2] accessible through
            telephone lines [...]")

        - A ordered list of page titles, that can be used for future
          dispatch.

        """
        links = []
        offset = 0
        output = bytes()
        for l in self.wiki_re.finditer(contents):
            title, _, linkto = l.group(1).partition("|")
            if linkto == "":
                linkto = title
            if linkto not in links:
                links.append(linkto)
                pos = len(links) - 1
            else:
                pos = links.index(title)
            sfrom, sto = l.span()
            output += (
                tc.abytes(contents[offset:sfrom]) +
                tc.tFgColor(tc.clCyan) +
                tc.abytes("%s[%d]" % (title, pos)) +
                tc.tFgColor(tc.clWhite)
            )
            offset = sto
        output += tc.abytes(contents[offset:])
        return output, links

    def get_page(self, title):
        with Session(GetEngine()) as session:
            title = normalize_wiki_title(title)
            p = session.query(WikiArticle).where(WikiArticle.title == title).first()
            return p

    def do_save(self, title):
        q = QuestEntry(nick=self.nick, quest=title)
        logging.debug("Saving quest record %s", q)
        try:
            with Session(GetEngine()) as session:
                session.add(q)
                session.commit()
        except:
            pass  # This happens when someone tries to submit twice. Ignore it.

        
    def render_page(self, title):
        p = self.get_page(title)
        if p is None:
            return
        logging.info("Wiki: navigating to %s", title)
        self.do_save(p.title)
        contents, links = self.linkify(p.contents)

        while True:
            self.m.reset()
            self.m.pos(2, 1)
            self.m._write(tc.ESC + tc.tSetDoubleSize)
            self.m.print(p.title)
            self.m.pos(24, 1)
            self.m.print("Titre ou num: " + '.' * WIKI_TITLE_MAXLEN)
            self.m.pos(24, 36)
            self.m.setInverse()
            self.m.print("ENVOI")
            self.m.pos(3, 1)
            self.m._write(contents)

            prompt = self.m.addInputField(24, 14, WIKI_TITLE_MAXLEN, "")
            self.m.keyHandlers[tc.kEnvoi] = tc.Break
            self.m.handleInputsUntilBreak()
            ck = self.m.lastControlKey()
            if ck == tc.kEnvoi:
                entry = prompt.contents.strip()
                try:
                    newtitle = links[int(entry)]
                except:
                    newtitle = entry
                self.render_page(newtitle)
                if self.m.lastControlKey() == tc.kSommaire:
                    # If we recursed out because kSommaire was pressed, break out of this loop
                    break
            elif ck == tc.kRetour or ck == tc.kSommaire:
                break
