# -*- coding: utf-8 -*-

from SupplierCache import SupplierCache
import json

class BaseSupplier:
    def __init__(self):
        self.name = "BaseSupplier"
        self.tag = "base"
        self.cachable = False

    def id(self):
        return "[{0}:{1}]".format(self.name, self.tag)

    def get(self):
        if self.cachable:
            data = SupplierCache.get(self.tag)
            if not data is None:
                return data

        data = self.tryGet()

        if self.cachable and not data is None:
            SupplierCache.save(self.tag, data)

        return data


    def tryGet(self):
        raise "Child Class Should Implements This Method"
