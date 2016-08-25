# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from lib import Logger
from BaseExtender import BaseExtender
from BaseSupplier import BaseSupplier


class MultiStageKeyExtender(BaseExtender):
    def __init__(self, tag, contexts):
        BaseExtender.__init__(self)
        self.name = "MultiStageKeyExtender"
        self.tag = tag
        self.contexts = contexts

        #print 'bk={0} dk={1} i={2}'.format(self.base_key_index, self.data_key_index, self.insert_index)

    def buildExtendDict(self, data, key_index):
        key_dict = {}
        for record in data:
	    row = list(record)
            key = row[key_index]
            row.pop(key_index)
            key_dict[str(key)] = row
        return key_dict

    def extendOneStage(self, context, data):
        base_data = context['supplier'].get()
        if base_data is None or len(base_data) == 0:
            return data

        key_dict = self.buildExtendDict(base_data, int(context['base_key_index']))

        result = []
	for row in data:
	    #Logger.df("", row)
            key = row[int(context['data_key_index'])]
	    if not key in key_dict:
		continue
            extends = key_dict[str(key)]
            i = int(context['insert_index'])
            for ext in extends:
                row.insert(i, ext)
                i = i + 1
            result.append(row)
        return result


    def extend(self, data):
        for context in self.contexts:
            data = self.extendOneStage(context, data)
        return data


class TestSupplier1(BaseSupplier):
    def tryGet(self):
        data = []
        data.append(["k1", "name 1", "alias 1"])
        data.append(["k2", "name 2", "alias 2"])
        data.append(["k3", "name 3", "alias 3"])
        return data

class TestSupplier2(BaseSupplier):
    def tryGet(self):
        data = []
        data.append(["r1", "record 1"])
        data.append(["r2", "record 2"])
        data.append(["r3", "record 3"])
        return data


if __name__ == "__main__":
    extender = MultiStageKeyExtender("TestExtender",
            [
                {"supplier":TestSupplier1(), "base_key_index":0, "data_key_index":0, "insert_index":1},
                {"supplier":TestSupplier2(), "base_key_index":0, "data_key_index":3, "insert_index":4}
            ]
        )
    data = []
    data.append(["k1", "r2", 123, 456])
    data.append(["k2", "r3", 235, 888])
    result = extender.extend(data)
    for row in result:
        rrow = []
        for item in row:
            rrow.append(str(item))
        print ','.join(rrow)


