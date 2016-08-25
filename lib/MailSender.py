# -*- coding: utf-8 -*-

import time
import urllib
import urllib2
import hashlib

#MAIL_APP = "native"
#MAIL_APP_KEY = "k3c7r9#d"
#MAIL_SERVER = "http://ips.ymtech.info/notify/api/semail"

MAIL_APP = "Native_Official"
MAIL_APP_KEY = "7cQKmUb1"
MAIL_SERVER = "http://notify.ymtech.info/notify/api/send"
FROM_NAME = "NATIVE"
FROM_EMAIL = "display_ads@ndpmedia.com"


'''
    @author: NGloom.Wu@ndpmedia.com
    
    参数说明：
    toList : 收件人列表
    title  : 邮件标题 
    body   : 邮件正文
        
        接口说明参考这里：http://ndp.confluence.dy/pages/viewpage.action?pageId=2523245
'''


def sendMail(toList, title, body):
    #print body
    # 计算签名值
    tm = str(int(time.time()))
    sign = MAIL_APP + MAIL_APP_KEY + tm
    sign = hashlib.md5(sign).hexdigest()[:8]

    mail = {}
    mail['to'] = ','.join(toList)
    mail['subject'] = title
    mail['body'] = body
    mail['app'] = MAIL_APP
    mail['time'] = tm
    mail['sign'] = sign
    mail['from'] = FROM_EMAIL
    mail['fromName'] = FROM_NAME

    req = urllib2.Request(MAIL_SERVER)
    data = urllib.urlencode(mail)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    print response.read()

    pass


if __name__ == "__main__":
    to = ["ulyx.yang@yeahmobi.com"]
    title = "Mail Sender Test"
    body = "This is body</br>This is body2" + time.ctime()

    sendMail(to, title, body)
