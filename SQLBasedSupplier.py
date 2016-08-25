# -*- coding: utf-8 -*-

from lib import Logger
from BaseSupplier import BaseSupplier
from lib import DBFactory


class SQLBasedSupplier(BaseSupplier):
    def __init__(self, tag, db_name, sql, cachable=False):
        BaseSupplier.__init__(self)
        self.name = "SQLBaseSupplier"
        self.tag = tag
        self.sql = sql
        self.db_name = db_name
        self.cachable = cachable

    def tryGet(self):

        db = None
        try:
            db = DBFactory.getInstance(self.db_name)

            if db is None:
                Logger.f(self.id(), "not suitable db instance: db=None")
                return None

            #Logger.d(self.id(), "[SQL]" + self.sql)
            i = 0
            tmp = self.sql.strip(';').split(';')
            sqls = []
            for sql in tmp:
                if sql is None:
                    continue
                if sql.strip() == '':
                    continue
                sqls.append(sql)
            while i < len(sqls) - 1:
                Logger.d(self.id(), sqls[i])
                cursor = db.cursor()
                cursor.execute(sqls[i])
                cursor.close()
                i = i + 1
            Logger.d(self.id(), sqls[i])
            cursor = db.cursor()
            cursor.execute(sqls[i])
            res_list = cursor.fetchall()
            return res_list
        finally:
            test = 0


