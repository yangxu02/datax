# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import MySQLdb
import datetime
import time
import sys 
from lib import DB
from lib import MailSender

def getSlotsUnapproved():
    db = DB.getSSPSlaveDb()
    sql = "select t1.id,t1.name,t1.app_id,t2.name,t1.created_time,t3.name,t3.contact_person,t3.mobile_phone_number,t3.qq_number,t3.skype_number from ssp_slot t1,ssp_app t2,ssp_user t3 where t1.app_id = t2.id and t2.user_id = t3.id and   t1.status = 2"
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    return resList

def gethtml(data):
    cssheader = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head><style type='text/css'>table.gridtable {   font-family: verdana,arial,sans-serif;  font-size:11px; color:#333333;  border-width: 1px;  border-color: #666666;  border-collapse: collapse;table-layout:fixed;}table.gridtable th { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #dedede;}table.gridtable td { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #ffffff;word-break: break-all; word-wrap:break-word;}</style></head><body>"
    content = cssheader
    content += "<p>Ngp Country Details:</p>"
    content += "<table class=\"gridtable\">"
    content += "<tr><th width=\"200\">slotId</th><th width=\"200\">slotName</th><th width=\"200\">appId</th><th width=\"200\">appName</th><th width=\"200\">created_time</th><th width=\"200\">username</th><th width=\"200\">contact_person</th><th width=\"200\">mobile_phone_number</th><th width=\"200\">qq_number</th><th width=\"200\">skype_number</th></tr>"
    for item in data:
        content +="<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"%(str(item[0]),item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9])
    content +="</table>"

    content +="</body></html>"
    
    return content

def sendEmail(html):
    to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;yuanbin@yeahmobi.com;steven.zhu@yeahmobi.com"]
    title = "[NATIVE SLOT UNAPPROVED]"
    MailSender.sendMail(to,title,html)

def mineall():
    print "==== The whole SLOT UNAPPROVED Process Start at " + time.ctime() + "===="

    try:       

        data = getSlotsUnapproved()
        if len(data) > 0:
            html = gethtml(data)
            sendEmail(html)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)    

    print "==== The whole SLOT UNAPPROVED End at " + time.ctime() + "===="
    

def run(op):
    if op == 'all':
        mineall()


def SQL_INFO(sql):
    print datetime.datetime.now(),"[SQL]", sql.encode('UTF-8')


def usage(msg):
    if msg != "":
        print "[ERROR]",msg
    print "Usage==============="
    print "python slot_status_notify.py [TYPE]"
    print 'TIME_TYPE:',"all"
    print "===================="
    sys.exit()

if __name__ == "__main__":

    argv = sys.argv[1:]

    if len(argv) < 1:
        usage("")

    op = argv[0]

    if op == 'all':       
        run(op)
    else:
        usage("Operation not supported "+op)  

    pass