# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker
from lib import HtmlFactory
from lib import MailSender


class EmailBasedSinker(BaseSinker):
    def __init__(self, tag, address, title, cols):
        BaseSinker.__init__(self)
        self.name = "EmailBasedSinker"
        self.tag = tag
        self.title = title
        self.cols = cols
        self.address = address

    def sink(self, data):
        if data is None or len(data) == 0:
            Logger.e(self.id(), "no data, abort")
            return
        cols = self.cols.split(',')
        content = HtmlFactory.gethtml(self.title, cols, data)
        title = "[%s]" % self.title
        mail_to = [self.address]
        #MailSender.sendMail2(mail_to, title, content)
        MailSender.sendMail(mail_to, title, content)

if __name__ == "__main__":
    testTag = "test"
    testTitle = "test email sinker"
    testCols = "col1, col2"
    testAddress = "ulyx.yang@ndpmedia.com"
    testSinker = EmailBasedSinker(testTag, testAddress, testTitle, testCols)
    testData = [["123", "456"], ["789", "100"]]
    testSinker.sink(testData)


