from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from absl import flags
from minitel.database import GetEngine, WikiArticle
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
import re

@register("wiki")
class WikiApp(BaseApp):
    wiki_re = re.compile("\[\[([^]]+)\]\]")

    def interact(self):
        return self.page("index")

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
                tc.ESC + tc.tStartUnderline +
                tc.abytes("%s[%d]" % (title, pos)) +
                tc.ESC + tc.tEndUnderline
            )
            offset = sto
        return output, links

    def page(self, title):
        with Session(GetEngine()) as session:
            p = session.query(WikiArticle).where(WikiArticle.title == title).first()
            if p is None:
                return self.page("index")
        self.m.reset()
        self.m.print(p.title)
        contents, links = self.linkify(p.contents)
        self.m._write(contents)
        self.m.handleInputsUntilBreak()
