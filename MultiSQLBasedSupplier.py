# -*- coding: utf-8 -*-

from lib import Logger
from BaseSupplier import BaseSupplier
from lib import DB
from lib import DBFactory


class MultiSQLBasedSupplier(BaseSupplier):
    def __init__(self, tag, db_name, sql_contexts, cachable = False):
        BaseSupplier.__init__(self)
        self.name = "MultiSQLBasedSupplier"
        self.tag = tag
        self.sql_contexts = sql_contexts
        self.db_name = db_name
        self.cachable = cachable

    def tryGet(self):
        db = DBFactory.getInstance(self.db_name)

        if db is None:
            Logger.f(self.id(), "not suitable db instance: db=None")
            return None

        #Logger.d(self.id(), "[SQL]" + self.sql)
        result = {}
        for key in self.sql_contexts:
            sql = self.sql_contexts[key]['sql']

            i = 0
            tmp = sql.strip(';').split(';')
            sqls = []
            for sql in tmp:
                if sql is None:
                    continue
                if sql.strip() == '':
                    continue
                sqls.append(sql)
            while i < len(sqls) - 1:
                print sqls[i]
                cursor = db.cursor()
                cursor.execute(sqls[i])
                cursor.close()
                i = i + 1
            print sqls[i]
            cursor = db.cursor()
            cursor.execute(sqls[i])
            res_list = cursor.fetchall()

            result[key] = res_list

        return result

