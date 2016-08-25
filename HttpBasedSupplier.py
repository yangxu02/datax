# -*- coding: utf-8 -*-

from lib import Logger
from BaseSupplier import BaseSupplier
import requests
import json


class HttpBasedSupplier(BaseSupplier):
    def __init__(self, tag, log_date='', product='np', dims='slot,adid', cq='req,click,conv', filters=None, cachable=False):
        BaseSupplier.__init__(self)
        self.name = "HttpBaseSupplier"
        self.tag = tag
        self.log_date = log_date
        self.product = product
        self.dims = dims.split(',')
        self.cq = cq.split(',')
        self.filters = filters
        self.cachable = cachable

    def buildQueryObject(self):
        #return {"rowkeys": keys.join(), "date":self.log_date, "product":self.product, "cq":cq}
        return {"date":self.log_date, "dimen":''.join(self.dims), "product":self.product, "cq":self.cq}

    def tryGet(self):
        body = self.buildQueryObject()
        Logger.d(self.id(), "query=" + json.dumps(body))
        resp = requests.post(url='http://10.1.11.100:8080/native_report/v2', data=json.dumps(body))
        content = resp.json()
        #print content
        data = []
        Logger.d(self.id(), "content size=" + str(len(content)))
        Logger.d(self.id(), "dimens=" + ','.join(self.dims))
        Logger.d(self.id(), "dimenFilters=" + ','.join(self.filters['slot']))
        for elem in content:
            cell = []
            cell.append(self.log_date)
            dimenValues = elem['dimenId'].split('|')
            i = 0
            while i < len(self.dims):
                dim = self.dims[i]
                dimValue = dimenValues[i]
                if not self.filters is None and 0 != len(self.filters):
                    if dim in self.filters:
                        if dimValue not in self.filters[dim]:
                            i = i + 1
                            continue
                cell.append(dimValue)
                i = i + 1
            if len(cell) != len(self.dims) + 1:
                continue
            i = 0
            while i < len(self.cq):
                cols = elem['columns']
                if self.cq[i] in cols:
                    cell.append(cols[self.cq[i]])
                else:
                    cell.append('0')
                i = i + 1
            data.append(cell)
        return data

if __name__ == "__main__":
    supplier = HttpBasedSupplier("test")
    supplier.tryGet()
