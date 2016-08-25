# -*- coding: utf-8 -*-


import MySQLdb
from lib import Logger

db_configs = {
    'dsp' : {'host':'dsp.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'dspadmin',"passwd":'Yna4o4AM0ljDAweZSYjJ','charset':'utf8','db':'dsp'},
    'dsp-slave' : {'host':'dspslave.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'dspadmin',"passwd":'Yna4o4AM0ljDAweZSYjJ','charset':'utf8','db':'dsp'},
    'dspreport' : {'host':'ec2-54-165-200-194.compute-1.amazonaws.com','port':3306,'user':'dsp_report',"passwd":'123456','charset':'utf8','db':'dsp_report'},
    'ssp' : {'host':'dsp.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'sspadmin',"passwd":'pAOTpxASnoRT','charset':'utf8','db':'ssp'},
    'ssp-slave' : {'host':'dspslave.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'sspadmin',"passwd":'pAOTpxASnoRT','charset':'utf8','db':'ssp'},
    'ssp-report' : {'host':'native-report.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'sspadmin',"passwd":'pAOTpxASnoRT','charset':'utf8','db':'ssp'},
    'ssp-report-slave' : {'host':'native-report-slave.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'sspadmin',"passwd":'pAOTpxASnoRT','charset':'utf8','db':'ssp'},
    'mana-slave' : {'host':'native-mana.cgs2bjzqxcxl.us-east-1.rds.amazonaws.com','port':3306,'user':'dev',"passwd":'t6W3dx8s5Dh4fmvR','charset':'utf8','db':'mana'},
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
