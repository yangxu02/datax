# -*- coding: utf-8 -*-

from lib import Logger
from BaseSinker import BaseSinker


class MultiSectionCsvSinker(BaseSinker):
    def __init__(self, tag, contexts):
        BaseSinker.__init__(self)
        self.name = "MultiSectionScvSinker"
        self.tag = tag
        self.contexts = contexts

    def sink(self, sections):
        if sections is None or len(sections) == 0:
            Logger.e(self.id() + "no data, abort")
            return
        for context in self.contexts:
            key = context["id"]
	    output_file = context["output"]
	    cols = context["cols"].split(",")
	    write_header = context["write_header"]
            section = sections[key]
	    with open(output_file, "w") as fp:
		if write_header:
		    print >> fp, '\t'.join(cols)
		for row in section:
		    rowdata = []
		    for item in row:
			rowdata.append(str(item))
		    print >> fp, '\t'.join(rowdata)

if __name__ == "__main__":
    testTag = "test"
    testTitle = "test email sinker"
    testContexts = [
	{"id": "s1", "output": "./test/s1.csv", "cols": "col1, col2", "write_header":True},
	{"id": "s2", "output": "./test/s2.csv", "cols": "colA, colB", "write_header":False}
    ]
    testSinker = MultiSectionCsvSinker(testTag, testContexts)
    testData = {
        "s1":[["123", "456"], ["789", "100"]],
        "s2":[["1123", "4156"], ["7189", "1100"]],
    }
    testSinker.sink(testData)


