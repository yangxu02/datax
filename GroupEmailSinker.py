# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker
from lib import HtmlFactory
from lib import MailSender


class GroupEmailSinker(BaseSinker):
    def __init__(self, tag, address, title, cols, group_by, limit):
        BaseSinker.__init__(self)
        self.name = "GroupEmailSinker"
        self.tag = tag
        self.cols = cols
        self.group_by = group_by
        self.limit = int(limit)
        self.address = address
        self.title = title

    def buildColIndex(self):
        col_index = {}
        col_array = self.cols.split(',')
        i = 0
        while i < len(col_array):
            col_index[col_array[i]] = i
            i = i + 1
        return col_index

    def buildDataGroup(self, data):
        col_index = self.buildColIndex()
        groups = self.group_by.split(',')
        indices = []
        for group in groups:
            indices.append(col_index[group])
        grouped_data = {}
        grouped_data['__meta__'] = []
        for row in data:
            key = "";
            for i in indices:
                key += "," + row[i]
            key = "(" + key[1:] + ")"
            if not key in grouped_data:
                section = {}
                section['title'] = '[Group](' + self.group_by + '):' + key
                section['cols'] = self.cols
                section['data'] = []
                section['data'].append(row)
                grouped_data[key] = section
                grouped_data['__meta__'].append(key)
            else:
                section = grouped_data[key]
                if len(section['data']) >= self.limit:
                    continue
                section['data'].append(row)
        return grouped_data

    def sink(self, data):
        if data is None or len(data) == 0:
            Logger.e(self.id() + "no data, abort")
            return
        sections = self.buildDataGroup(data)
        keys = sections['__meta__']
        content = ""
        #for key in sections:
        for key in keys:
            section = sections[key]
            content += "</p>"
            content += HtmlFactory.getTable(section["title"], section['cols'].split(','), section['data'])

        content = HtmlFactory.getHeader(content)
	#print content

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


