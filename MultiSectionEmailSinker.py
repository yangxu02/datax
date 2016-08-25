# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker
from lib import HtmlFactory
from lib import MailSender


class MultiSectionEmailSinker(BaseSinker):
    def __init__(self, tag, address, title, contexts):
        BaseSinker.__init__(self)
        self.name = "MultiSectionEmailSinker"
        self.tag = tag
        self.contexts = contexts
        self.address = address
        self.title = title

    def sink(self, sections):
        if sections is None or len(sections) == 0:
            Logger.e(self.id() + "no data, abort")
            return
        content = ""
        for context in self.contexts:
            key = context["id"]
            section = sections[key]
            content += "</p>"
            content += HtmlFactory.getTable(context["title"], context['cols'].split(','), section)

        content = HtmlFactory.getHeader(content)

        title = "[%s]" % self.title
        mail_to = [self.address]
        #MailSender.sendMail2(mail_to, title, content)
        MailSender.sendMail(mail_to, title, content)

if __name__ == "__main__":
    testTag = "test"
    testTitle = "test email sinker"
    testContexts = [ {"id":"s1", "title": "section 1", "cols": "col1, col2"}, {"id":"s2", "title": "section 2", "cols": "colA, colB"} ]
    testAddress = "ulyx.yang@ndpmedia.com"
    testSinker = MultiSectionEmailSinker(testTag, testAddress, testTitle, testContexts)
    testData = { "s1":[["123", "456"], ["789", "100"]], "s2":[["1123", "4156"], ["7189", "1100"]], }
    testSinker.sink(testData)


