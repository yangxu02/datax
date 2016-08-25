# -*- coding: utf-8 -*-

from lib import Logger
import datetime
import os
import os.path
import sys
import json
import pickle

cache_dir = './cache/'

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

class SupplierCache:
    @staticmethod
    def getPath(tag):
        suffix = str(datetime.date.today())
        return (cache_dir + suffix + '.' + tag)


    @staticmethod
    def save(tag, data):
        if data is None:
            return
        fileName = SupplierCache.getPath(tag)
        print fileName
        with open(fileName, 'wb') as fp:
            pickle.dump(data, fp)

    @staticmethod
    def get(tag):
        fileName = SupplierCache.getPath(tag)
        if not os.path.exists(fileName):
            return None
        statinfo = os.stat(fileName)
        if statinfo.st_size == 0:
            return None
        with open(fileName, 'rb') as fp:
            return pickle.load(fp)
            #data = fp.read()
            #if data is None or data == '':
            #    return None

