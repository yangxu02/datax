# -*- coding: utf-8 -*-


class BaseExtender:
    def __init__(self):
        self.name = "BaseExtender"
        self.tag = "base"

    def id(self):
        return "[{0}:{1}]".format(self.name, self.tag)

    def extend(self, data):
        raise "Child Class Should Implements This Method"
