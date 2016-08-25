# -*- coding: utf-8 -*-


class BaseSinker:
    def __init__(self):
        self.name = "BaseNotify"
        self.tag = "base"

    def id(self):
        return "[{0}:{1}]".format(self.name, self.tag)

    def sink(self, data):
        raise "Child Class Should Implements This Method"
