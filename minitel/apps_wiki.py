from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from absl import flags
from minitel.database import GetEngine, WikiArticle, WIKI_TITLE_MAXLEN, normalize_wiki_title
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
import re


@register("wiki")
class WikiApp(BaseApp):
    wiki_re = re.compile("\[\[([^]]+)\]\]")

    def interact(self):
        return self.render_page("index")

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
            print("%s at %s" % (repr(l), l.span()))
            title, _, linkto = l.group(1).partition("|")
            if linkto == "":
                linkto = title
            if linkto not in links:
                links.append(linkto)
                pos = len(links) - 1
            else:
                pos = links.index(title)
            print("%s[%d] -> %s" % (title, pos, linkto))
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

    def render_page(self, title):
        print("Page: ", title)
        p = self.get_page(title)
        if p is None:
            return
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
