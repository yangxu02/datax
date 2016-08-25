# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from lib import Logger
from BaseExtender import BaseExtender
from BaseSupplier import BaseSupplier


class KeyBasedExtender(BaseExtender):
    def __init__(self, tag, supplier, base_key_index, data_key_index, insert_index):
        BaseExtender.__init__(self)
        self.name = "KeyBasedExtender"
        self.tag = tag
        self.supplier = supplier
        self.base_key_index = int(base_key_index)
        self.data_key_index = int(data_key_index)
        self.insert_index = int(insert_index)

        #print 'bk={0} dk={1} i={2}'.format(self.base_key_index, self.data_key_index, self.insert_index)

    def buildExtendDict(self, data, key_index):
        key_dict = {}
        for record in data:
	    row = list(record)
            key = row[key_index]
            row.pop(key_index)
            key_dict[str(key)] = row
        return key_dict

    def extend(self, data):
        base_data = self.supplier.get()
        if base_data is None or len(base_data) == 0:
            return data

        key_dict = self.buildExtendDict(base_data, self.base_key_index)

        result = []
        for row in data:
            key = row[self.data_key_index]
	    if not key in key_dict:
		continue
            extends = key_dict[str(key)]
            i = self.insert_index
            for ext in extends:
                row.insert(i, ext)
                i = i + 1
            result.append(row)
        return result


class TestSupplier(BaseSupplier):
    def tryGet(self):
        data = []
        data.append(["k1", "name 1", "alias 1"])
        data.append(["k2", "name 2", "alias 2"])
        data.append(["k3", "name 3", "alias 3"])
        return data


if __name__ == "__main__":
    extender = KeyBasedExtender("TestExtender", TestSupplier(), 0, 0, 1)
    data = []
    data.append(["k1", 123, 456])
    data.append(["k2", 235, 888])
    result = extender.extend(data)
    for row in result:
        rrow = []
        for item in row:
            rrow.append(str(item))
        print ','.join(rrow)


