# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from lib import Logger
from BaseSupplier import BaseSupplier


class HiveBasedSupplier(BaseSupplier):
    def __init__(self, tag, db_name, sql, tmp_dir=None, cachable=False):
        BaseSupplier.__init__(self)
        self.name = "HiveBaseSupplier"
        self.tag = tag
        self.sql = sql
        self.db_name = db_name
        self.tmp_dir = tmp_dir
        if self.tmp_dir is None:
            self.tmp_dir = './tmp/' + self.tag
        self.cachable = cachable

    def tryLoadFromHiveToLocalFile(self):
        sql = "use {0};".format(self.db_name)
        i = 0
        tmp = self.sql.strip(';').split(';')
        sqls = []
        for sql_tmp in tmp:
            if sql_tmp is None:
                continue
            if sql_tmp.strip() == '':
                continue
            sqls.append(sql_tmp.strip('\r').strip('\n'))
        while i < len(sqls) - 1:
            sql += sqls[i] + ";"
            i = i + 1

        sql += " INSERT OVERWRITE LOCAL DIRECTORY '{0}' ".format(self.tmp_dir)
        #sql += sqls[i].replace("\n", "").replace("\r", "") + ";"
        sql += sqls[i] + ";"
	Logger.d(self.id(), sql)
	Logger.d(self.id(), "tmp_dir=" + self.tmp_dir)
        #child = subprocess.Popen(['mkdir', self.tmp_dir, '-p'])
        child1 = subprocess.Popen(['hive', '-e ' + sql])
        child1.wait()

    def tryLoadFromLocalTempFile(self):
        data = []
	path = os.path.join(os.path.dirname(__file__), self.tmp_dir)
        for file in os.listdir(path):
	    if not os.path.isfile(path + '/' + file):
		print file
                continue
	    if file.find("crc") >= 0:
                continue
            with open(path + '/' + file) as f:
                for line in f:
                    line = line[:-1]
		    line = line.replace('\\N', '-')
                    comps = line.split('\x01')
                    data.append(comps)
        return data
                    
    def tryGet(self):

        self.tryLoadFromHiveToLocalFile()

        data = self.tryLoadFromLocalTempFile()

        Logger.w(self.id(), "data size=" + str(len(data)))

        return data


