# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker
from lib import HtmlFactory
from lib import RichHtmlFactory
from lib import C3ChartFactory
import json


class HttpBasedSinker(BaseSinker):
    def __init__(self, tag, title, cols, html_format="simple"):
        BaseSinker.__init__(self)
        self.name = "HttpBasedSinker"
        self.tag = tag
        self.title = title
        self.cols = cols
        self.html_format = html_format

    def sink(self, data):
        if data is None:
            Logger.e(self.id(), "no data, abort")
            return
        cols = self.cols.split(',')
        content = ""
        if "rich" == self.html_format:
            content = RichHtmlFactory.gethtml(self.title, cols, data)
        elif "c3" == self.html_format:
            content = C3ChartFactory.getHtml(self.title, cols, data)
        else:
            content = HtmlFactory.gethtml(self.title, cols, data)
        return content
