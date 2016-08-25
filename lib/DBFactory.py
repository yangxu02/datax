# -*- coding: utf-8 -*-


import MySQLdb
from lib import Logger

db_configs = {
    'test' : {'host':'test.com','port':3306,'user':'testuser',"passwd":'testpwd','charset':'utf8','db':'test'},
}

db_instances = {}

def connect(conf):
    instance = MySQLdb.Connect(host=conf['host'],port=conf['port'],user=conf['user'],passwd=conf['passwd'],charset=conf['charset'],db=conf['db'])
    instance.autocommit(True)
    return instance


def getInstance(db_name):
    global db_instances
    global db_configs
    if db_name not in db_configs:
        Logger.f("[DBFactory]", "unknown db instance")
        return None

    instance = None
    conf = db_configs[db_name]
    if db_name in db_instances:
        instance = db_instances[db_name]
    if instance is None:
        instance = connect(conf)
        db_instances[db_name] = instance
    else:
        try:
            instance.ping()
        except:
            instance = connect(conf)

    return instance

def release(instance):
    if instance is None:
        return
    instance.close()
