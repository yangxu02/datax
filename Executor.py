# -*- coding: utf-8 -*-

import datetime
import time
import sys

from Worker import Worker
from lib import Logger
from BaseSupplier import BaseSupplier


class Executor:
    def __init__(self, conf_file):
        self.worker = Worker(conf_file)

    def setUp(self):
        pass

    def run(self, task):
        self.worker.run(task)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        Logger.e("[Main]", "no enough argument given, exit")
        sys.exit(1)
    conf_file = sys.argv[1]
    task = sys.argv[2]
    executor = Executor(conf_file)
    executor.setUp()
    executor.run(task)


class SimpleTestSupplier(BaseSupplier):
    def get(self):
        return [["val1", "val2"], ["val3", "val4"]]

def test():

    config = '''
[task1]
supplier.type = test
sinker.type = email
sinker.title = executor test task1
sinker.cols = col1,col2
sinker.address = ulyx.yang@ndpmedia.com
[task2]
supplier.type = test
sinker.type = email
sinker.title = executor test task2
sinker.cols = col1,col2
sinker.address = ulyx.yang@ndpmedia.com
    '''

    with open("test.conf", "w") as wfp:
        wfp.write(config)

    executor = Executor("test.conf")
    executor.setUp()
    executor.run("task1")
    executor.run("task2")



