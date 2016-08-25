# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker
from lib import HtmlFactory


class MultiSectionHttpSinker(BaseSinker):
    def __init__(self, tag, title, contexts):
        BaseSinker.__init__(self)
        self.name = "MultiSectionHttpSinker"
        self.tag = tag
        self.contexts = contexts
        self.title = title

    def sink(self, sections):
        if sections is None:
            Logger.e(self.id() + "no data, abort")
            return
        content = ""
        for context in self.contexts:
            key = context["id"]
            section = sections[key]
            content += "</p>"
            content += HtmlFactory.getTable(context["title"], context['cols'].split(','), section)

        content = HtmlFactory.getHeader(content)

        return content
