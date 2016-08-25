# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import datetime
import time
import sys 
import os
from lib import DB
from lib import MailSender
from lib import Annotations

isdebug = False
PushSdkCountryFillratioFolder = '/dianyi/data/country_fill_rate'

def getData(sql):
    db = DB.getSSPReportDb()
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    return resList    

def getDspData(sql):
    db = DB.getDSPSlaveDb()
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    return resList

def getSSPSlaveData(sql):
    db = DB.getSSPSlaveDb()
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    return resList    

def getSSPReportSlaveData(sql):
    db = DB.getSSPReportSlaveDb()
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()
    return resList    

def gethtml(title,columns,data):
    cssheader = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head><style type='text/css'>table.gridtable {   font-family: verdana,arial,sans-serif;  font-size:11px; color:#333333;  border-width: 1px;  border-color: #666666;  border-collapse: collapse;table-layout:fixed;}table.gridtable th { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #dedede;}table.gridtable td { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #ffffff;word-break: break-all; word-wrap:break-word;}</style></head><body>"
    content = cssheader
    content += getTable(title,columns,data)
    content +="</body></html>"

    return content

def getHeader(html):
    cssheader = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head><style type='text/css'>table.gridtable {   font-family: verdana,arial,sans-serif;  font-size:11px; color:#333333;  border-width: 1px;  border-color: #666666;  border-collapse: collapse;table-layout:fixed;}table.gridtable th { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #dedede;}table.gridtable td { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #ffffff;word-break: break-all; word-wrap:break-word;}</style></head><body>"
    content = cssheader
    content += html
    content +="</body></html>"

    return content

def getTable(title,columns,data,option=None):
    if data is None or len(data) == 0:
        return ''
    content = ''
    content += "<p>%s:</p>"%title
    content += "<table class=\"gridtable\">"
    content += "<tr>%s</tr>"%(''.join(["<th width=\"200\">%s</th>"%str(name) for name in columns]))
    for row in data:
        rowdata =[]
        for i,item in enumerate(list(row)):
            tdc = str(item)
            if option is not None and option.has_key(columns[i]):
                if option[columns[i]] == 'img':
                    tdc = "<img src='%s' />"%str(item)
            td =  "<td>%s</td>"%tdc
            rowdata.append(td)
        content +="<tr>%s</tr>"%(''.join(rowdata))
    content +="</table>"
    return content

def sendEmail(title ,html, to=None):
    if to is None:
        to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com"]
    if isdebug == True:
        to = ["steven.zhu@yeahmobi.com;ulyx.yang@yeahmobi.com"]
    title = "[%s]"%title
    MailSender.sendMail(to,title,html)

def getpreviousDate(num):
    otherday = (datetime.datetime.now() - datetime.timedelta(days = num))
    styleTime = otherday.strftime("%Y-%m-%d")
    return styleTime

def getpreviousDate2(num):
    otherday = (datetime.datetime.now() - datetime.timedelta(days = num))
    styleTime = otherday.strftime("%Y%m%d")
    return styleTime

def getSlotFillRateLow():
    sql = " select * from (  select slot_id,requests,clicks,conversions,price,create_time,dau,ads_fill,ads_notfill,  if((ads_fill+ads_notfill)=0,0,ads_fill/(ads_fill+ads_notfill)) as fill_rate  from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(now(),'%Y-%m-%d') group by slot_id  ) ) t where fill_rate<0.8 order by requests desc"
    return getData(sql)

def getCountryRequestTop5():
    sql = " select * from (  select concat('top-request-5-',UPPER(country)),requests,clicks,conversions,ads_fill,ads_notfill,  if((ads_fill+ads_notfill)=0,0,ads_fill/(ads_fill+ads_notfill)) as fill_rate  from native_realtime_country_report where id in (  select max(id) from native_realtime_country_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d') group by country  ) ) t where requests >100000  order by requests desc limit 5"
    return getData(sql)

def getCountryFillRateTop5():
    sql = " select * from (  select concat('top-fillrate-5-',UPPER(country)),requests,clicks,conversions,ads_fill,ads_notfill,  if((ads_fill+ads_notfill)=0,0,ads_fill/(ads_fill+ads_notfill)) as fill_rate  from native_realtime_country_report where id in (  select max(id) from native_realtime_country_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d') group by country  ) ) t where requests >100000  order by fill_rate desc limit 5"
    return getData(sql)

def getCountryFillRateBottom5():
    sql = " select * from (  select concat('bottom-fillrate-5-',UPPER(country)),requests,clicks,conversions,ads_fill,ads_notfill,  if((ads_fill+ads_notfill)=0,0,ads_fill/(ads_fill+ads_notfill)) as fill_rate  from native_realtime_country_report where id in (  select max(id) from native_realtime_country_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d') group by country  ) ) t where requests >100000  order by fill_rate asc limit 5"
    return getData(sql)

def getCountryFillRateAll():
    sql = " select 'ALL' as country,requests,clicks,conversions,ads_fill,ads_notfill, if((ads_fill+ads_notfill)=0,0,ads_fill/(ads_fill+ads_notfill)) as fill_rate   from (  select sum(requests) requests,sum(clicks) clicks,sum(conversions) conversions,sum(ads_fill) ads_fill,sum(ads_notfill) ads_notfill  from native_realtime_country_report where id in (  select max(id) from native_realtime_country_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')  group by country ) ) t "
    return getData(sql)

def getDspAdUnapproved():
    sql = "select id,advertiser_id,ad_name,click_through_url,domain,updated_time from dsp_ad where is_valid='Y' and approved=0"
    return getDspData(sql)

def getDspCreativeUnapproved():
    sql = "select t1.id,t1.ad_id,t2.ad_name,t2.click_through_url,t1.title,CONCAT('http://d3bascu0xweno1.cloudfront.net/creatives',t1.img_url) as img_url,t1.width,t1.height,t1.updated_time from dsp_creative t1 left join dsp_ad t2 on t1.ad_id=t2.id  where t1.is_valid='Y' and t1.approved=0 and t2.is_valid='Y'"
    return getDspData(sql)

def getTargetTrafficTypeFillRate():
    sql = "select t2.target_traffic_type, sum(t1.requests) requests, sum(t1.clicks) clicks, sum(t1.conversions) conversions, sum(t1.ads_fill) ads_fill, sum(t1.ads_notfill) ads_notfill, if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type order by t2.target_traffic_type asc  "
    return getData(sql)

def getTargetTrafficTypeFillRateLast7day():
    sql = "select t1.target_traffic_type,t1.fill_rate,t2.fill_rate,t3.fill_rate,t4.fill_rate,t5.fill_rate,t6.fill_rate,t7.fill_rate from  ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t1 left join ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 2 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t2 on t1.target_traffic_type = t2.target_traffic_type left join (  select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 3 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t3 on t2.target_traffic_type = t3.target_traffic_type left join ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 4 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t4 on t3.target_traffic_type = t4.target_traffic_type left join ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 5 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t5 on t4.target_traffic_type = t5.target_traffic_type left join ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 6 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t6 on t5.target_traffic_type = t6.target_traffic_type left join ( select t2.target_traffic_type,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id group by  t2.target_traffic_type ) t7 on t6.target_traffic_type = t7.target_traffic_type "
    return getData(sql)

def getUnionStatus():
    sql = "select t2.advertiser_name,max(t1.created_time) as  last_import_time,max(t1.updated_time) as last_updated_time,TO_DAYS(NOW()) - TO_DAYS( max(t1.created_time)) as days_import_until_now,TO_DAYS(NOW()) - TO_DAYS(max(t1.updated_time)) as days_update_until_now,count(0) as ad_count from native_ad t1 left join native_advertiser t2 on t1.advertiser_id=t2.id  where t1.is_valid='Y' and t2.is_valid='Y' and t1.status=1 group by t2.advertiser_name order by count(0) desc  "
    return getSSPSlaveData(sql)

def getSlotFillRateYesterday():
    slotids = '23123,23162,23163'
    sql = "select t1.slot_id, sum(t1.requests) requests, sum(t1.clicks) clicks, sum(t1.conversions) conversions, sum(t1.ads_fill) ads_fill, sum(t1.ads_notfill) ads_notfill, if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id order by t1.slot_id asc "
    sql = sql%slotids
    return getData(sql)

def getSlotFillRateLast7day():
    slotids = '23123,23162,23163'
    sql = "select t1.slot_id,t1.fill_rate,t2.fill_rate,t3.fill_rate,t4.fill_rate,t5.fill_rate,t6.fill_rate,t7.fill_rate from   ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 1 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s)  group by  t1.slot_id ) t1  left join  ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 2 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t2 on t1.slot_id = t2.slot_id  left join  (  select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 3 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t3 on t2.slot_id = t3.slot_id  left join  ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 4 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t4 on t3.slot_id = t4.slot_id  left join  ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 5 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t5 on t4.slot_id = t5.slot_id  left join  ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 6 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t6 on t5.slot_id = t6.slot_id  left join  ( select t1.slot_id,  if((sum(t1.ads_fill)+sum(t1.ads_notfill))=0,0,sum(t1.ads_fill)/(sum(t1.ads_fill)+sum(t1.ads_notfill))) as fill_rate  from  ( select * from native_realtime_slot_report where id in (  select max(id) from native_realtime_slot_report where log_date=DATE_FORMAT(date_sub(curdate(),interval 7 day),'%%Y-%%m-%%d') group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id where t1.slot_id  in (%s) group by  t1.slot_id ) t7 on t6.slot_id = t7.slot_id "
    sql = sql%(slotids,slotids,slotids,slotids,slotids,slotids,slotids)
    return getData(sql)

def getNativeCreativeAll():
    sql = "select CONCAT(t1.width,'x',t1.height),count(0),count(distinct(t1.ad_id)),count(distinct(t2.bundle)) from native_creative t1 left join native_ad t2 on t1.ad_id = t2.id left join native_advertiser t3 on t2.advertiser_id = t3.id where t2.is_valid='Y' and t2.`status`=1 and t1.is_valid='Y' and t3.is_valid='Y' and  t1.img_url<>'' and t1.img_url is not null and t2.target_traffic_type=1 group by CONCAT(t1.width,'x',t1.height) order by count(0) desc "
    return getData(sql)

def getNativeCreativeNGP():
    sql = "select CONCAT(t1.width,'x',t1.height),count(0),count(distinct(t1.ad_id)),count(distinct(t2.bundle)) from native_creative t1 left join native_ad t2 on t1.ad_id = t2.id left join native_advertiser t3 on t2.advertiser_id = t3.id where t2.is_valid='Y' and t2.`status`=1 and t1.is_valid='Y' and t3.is_valid='Y' and  t1.img_url<>'' and t1.img_url is not null and t2.target_traffic_type=1 and t1.ad_id in (select DISTINCT(ad_id) from native_ngp_flags where ngp=1 and is_deleted=0 ) group by CONCAT(t1.width,'x',t1.height) order by count(0) desc"
    return getData(sql)

def getPushCreativeAll():
    sql = "select CONCAT(t1.width,'x',t1.height),count(0),count(distinct(t1.ad_id)),count(distinct(t2.bundle)) from native_creative t1 left join native_ad t2 on t1.ad_id = t2.id left join native_advertiser t3 on t2.advertiser_id = t3.id where t2.is_valid='Y' and t2.`status`=1 and t1.is_valid='Y' and t3.is_valid='Y' and  t1.img_url<>'' and t1.img_url is not null and t2.target_traffic_type=2 group by CONCAT(t1.width,'x',t1.height) order by count(0) desc"
    return getData(sql)

def getPushCreativeNGP():
    sql = "select CONCAT(t1.width,'x',t1.height),count(0),count(distinct(t1.ad_id)),count(distinct(t2.bundle)) from native_creative t1 left join native_ad t2 on t1.ad_id = t2.id left join native_advertiser t3 on t2.advertiser_id = t3.id where t2.is_valid='Y' and t2.`status`=1 and t1.is_valid='Y' and t3.is_valid='Y' and  t1.img_url<>'' and t1.img_url is not null and t2.target_traffic_type=2 and t1.ad_id in (select DISTINCT(ad_id) from native_ngp_flags where ngp=1 and is_deleted=0 ) group by CONCAT(t1.width,'x',t1.height) order by count(0) desc"
    return getData(sql)

def getPushNotificationData1(startDate):
    sql = "select FROM_UNIXTIME(date, '%%Y-%%m-%%d') as day, slot_id,case slot_id when 23544 then '1.0' else '1.2' end, left(income/push*1000,3) as ecpm, left(income/dau*10000,5) as `收入/10000DAU`, concat(left(ads_fill/request*100,5), '%%') as `填充率`, concat(left(dau_download/dau*100,5), '%%') as `联wifi用户占比`,left(get_ad_ok/dau,3) as `人均返回广告数`,concat(left(end_download_success/start_download*100,5), '%%') as `下载成功率`, concat(left(push_click/push*100,5), '%%') as `CTR`, concat(left(install/push_click*100,5), '%%') as `安装成功率`, concat(left(conversion/install*100,5), '%%') as `确认率` from native_report_daily_feed_performance where slot_id in (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') and date >= UNIX_TIMESTAMP('%s') order by slot_id,FROM_UNIXTIME(date, '%%Y-%%m-%%d')"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationData2(startDate):
    sql = "select FROM_UNIXTIME(date, '%%Y-%%m-%%d') as day, slot_id,case slot_id when 23544 then '1.0' else '1.2' end,  dau as `请求广告DAU`, request as `全部请求数`, ads_fill as `有效广告请求数`,  concat(left(ads_fill/request*100,5), '%%') as `填充率`, get_ad_ok as `服务端返回广告数`, left(get_ad_ok/dau,3) as `人均返回广告数` from native_report_daily_feed_performance where slot_id in (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') and date >= UNIX_TIMESTAMP('%s') order by slot_id,FROM_UNIXTIME(date, '%%Y-%%m-%%d')"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationData3(startDate):
    sql = "SELECT FROM_UNIXTIME(date, '%%Y-%%m-%%d') AS DAY, slot_id,case slot_id when 23544 then '1.0' else '1.2' end,  add_download AS `添加到下载队列广告数`, dau_download AS `下载开始DAU`, concat( LEFT (dau_download / dau * 100, 5), '%%' ) AS `连wifi用户占比`, start_download AS `开始下载广告数`, concat( LEFT ( start_download / add_download * 100, 5 ), '%%' ) AS `开始下载比率`, end_download_success AS `下载成功广告数`, LEFT (start_download / dau_download, 3) AS `人均下载次数`, concat( LEFT ( end_download_success / start_download * 100, 5 ), '%%' ) AS `下载成功率` FROM native_report_daily_feed_performance WHERE slot_id IN (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') AND date >= UNIX_TIMESTAMP('%s') ORDER BY slot_id,FROM_UNIXTIME(date, '%%Y-%%m-%%d')"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationData4(startDate):
    sql = "SELECT FROM_UNIXTIME(date, '%%Y-%%m-%%d') AS DAY, slot_id,case slot_id when 23544 then '1.0' else '1.2' end,  push AS `推送成功广告数`, push_click AS `消息栏点击数`, concat( LEFT (push_click / push * 100, 5), '%%' ) AS `CTR`, get_referrer_success AS `getreferrer成功广告数`, concat( LEFT ( get_referrer_success / push_click* 100, 5 ), '%%' ) AS `getreferrer成功率`, install_user_accept AS `点击安装的广告数`,concat(left(install_user_accept/get_referrer_success*100,5), '%%') as `用户选择安装比率` , install AS `安装成功的广告数`, concat(left(install/push_click*100,5), '%%') as `安装成功率` FROM native_report_daily_feed_performance WHERE slot_id IN (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') AND date >= UNIX_TIMESTAMP('%s') order by slot_id,FROM_UNIXTIME(date, '%%Y-%%m-%%d')"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationData5(startDate):
    sql = "SELECT FROM_UNIXTIME(date, '%%Y-%%m-%%d') AS DAY, slot_id,case slot_id when 23544 then '1.0' else '1.2' end,  add_download AS `添加到下载队列广告数`, send_referrer AS `referrer发送成功数`, concat( LEFT (send_referrer / install* 100, 5), '%%' ) AS `referrer发送成功率`, conversion AS `转化广告数`, concat( LEFT ( conversion / install * 100, 5 ), '%%' ) AS `确认率`, concat( LEFT ( conversion / push_click * 100, 5 ), '%%' ) AS `转化率` FROM native_report_daily_feed_performance WHERE slot_id IN (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') AND date >= UNIX_TIMESTAMP('%s') ORDER BY slot_id,FROM_UNIXTIME(date, '%%Y-%%m-%%d')"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationDataForBD(startDate):
    sql = "select FROM_UNIXTIME(t1.date, '%%Y-%%m-%%d') as day, t4.name as user_name,t4.company,t2.name as slot_name, left(t1.income/t1.push*1000,5) as ecpm,t1.income,left(t1.income/t1.conversion,5),t1.dau, left(t1.income/t1.dau*10000,5) as `收入/10000DAU`, concat(left(t1.ads_fill/t1.request*100,5), '%%') as `填充率`, concat(left(t1.dau_download/t1.dau*100,5), '%%') as `联wifi用户占比`,left(t1.get_ad_ok/t1.dau,3) as `人均返回广告数`,concat(left(t1.end_download_success/t1.start_download*100,5), '%%') as `下载成功率`, concat(left(t1.push_click/t1.push*100,5), '%%') as `CTR`, concat(left(install/t1.push_click*100,5), '%%') as `安装成功率`, concat(left(t1.conversion/t1.install*100,5), '%%') as `确认率` from native_report_daily_feed_performance t1 left join ssp_slot t2 on t1.slot_id = t2.id left join ssp_app t3 on t2.app_id = t3.id left join ssp_user t4 on t3.user_id = t4.id  where t1.slot_id in (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') and t1.date = UNIX_TIMESTAMP('%s') order by t4.id"%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushNotificationDataForBDTotal(startDate):
    sql = "select 'Total:', '-','-','-', left(sum(t1.income)/sum(t1.push)*1000,5) as ecpm,left(sum(t1.income),7),left(sum(t1.income)/sum(t1.conversion),5),concat(sum(t1.dau),'(未去重)'), concat(left(sum(t1.income)/sum(t1.dau)*10000,5),'(未去重)'), concat(left(sum(t1.ads_fill)/sum(t1.request)*100,5), '%%') as `填充率`, '-','-',concat(left(sum(t1.end_download_success)/sum(t1.start_download)*100,5), '%%') as `下载成功率`, concat(left(sum(t1.push_click)/sum(t1.push)*100,5), '%%') as `CTR`, concat(left(sum(install)/sum(t1.push_click)*100,5), '%%') as `安装成功率`, concat(left(sum(t1.conversion)/sum(t1.install)*100,5), '%%') as `确认率` from native_report_daily_feed_performance t1 left join ssp_slot t2 on t1.slot_id = t2.id left join ssp_app t3 on t2.app_id = t3.id left join ssp_user t4 on t3.user_id = t4.id  where t1.slot_id in (select id from ssp_slot where notes like '%%Yeahmobi_PushSDK_1.2.0%%') and t1.date = UNIX_TIMESTAMP('%s') "%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getDailyCountryPushSdkData(startDate):
    sql = "select countryCode,income,dau from native_report_daily_country_pushsdk where date = UNIX_TIMESTAMP('%s') "%(startDate)
    print sql
    return getSSPReportSlaveData(sql)

def getPushSlotAdConfirmRate():
    date_diff = '1'
    sql ="select  t1.ad_id, t2.ad_name, t2.bundle, t2.ad_cpa_bid, t1.impression, t1.click, ifnull(round(if(t1.impression=0,0,t1.click/t1.impression),4),0) as ctr,   t1.get_referrer, ifnull(round(if(click=0,0,t1.get_referrer/t1.click),4),0) as referrerRate, t1.install, t1.conversion, ifnull(round(if(t1.install=0,0,t1.conversion/t1.install),8),0) as confirmRate,  ifnull(round(if(click=0,0,conversion/click),4),0) as cvr,  ifnull(round(if(t1.impression=0,0,t1.income/t1.impression)*1000,4),0) as ecpm, t1.income from  ( select ad_id , sum(ifnull(impression,0)) impression, sum(ifnull(click,0)) click, sum(ifnull(get_referrer,0)) get_referrer, sum(ifnull(install,0)) install, sum(ifnull(conversion,0)) conversion, sum(ifnull(income,0)) income from ( select ad_id, impression, click, get_referrer, install, conversion, income from bi_report_push_ad_cny where DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(date)  and type='push_sdk'  union all select ad_id, 0 as impression, 0 as click, 0 as get_referrer, 0 as install, conversion, income  from native_report_daily_income_apk where  DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(created_time) and is_valid='Y' ) t0 group by ad_id ) t1 left join native_ad t2 on t1.ad_id = t2.id  order by t1.install desc limit 120; "%(date_diff,date_diff)
    print sql
    return getSSPReportSlaveData(sql)

def getPushSlotAdConfirmRateByCountry(country):
    date_diff = '1'
    sql = "select ifnull(round(if(t2.income=0,0,t1.income/t2.income),8),0) from  (select 'a' as id,sum(income) as income from bi_report_push_ad_cny where DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(date)  and type='push_sdk' and country='%s' ) t1 left join  (select 'a' as  id,sum(income) as income from bi_report_push_ad_cny where DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(date)  and type='push_sdk') t2 on t1.id = t2.id"%(date_diff,country,date_diff)
    db = DB.getSSPReportDb()
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    ratio = str(cursor.fetchone()[0])

    sql = "select  t1.ad_id, t2.ad_name, t2.bundle, t2.ad_cpa_bid, t1.impression, t1.click, ifnull(round(if(t1.impression=0,0,t1.click/t1.impression),4),0) as ctr,   t1.get_referrer, ifnull(round(if(click=0,0,t1.get_referrer/t1.click),4),0) as referrerRate, t1.install, t1.conversion, ifnull(round(if(t1.install=0,0,t1.conversion/t1.install),8),0) as confirmRate,  ifnull(round(if(click=0,0,conversion/click),4),0) as cvr,  ifnull(round(if(t1.impression=0,0,t1.income/t1.impression)*1000,4),0) as ecpm, t1.income from  ( select ad_id , sum(ifnull(impression,0)) impression, sum(ifnull(click,0)) click, sum(ifnull(get_referrer,0)) get_referrer, sum(ifnull(install,0)) install, sum(ifnull(conversion,0)) conversion, sum(ifnull(income,0)) income from ( select ad_id, impression, click, get_referrer, install, conversion, income from bi_report_push_ad_cny where DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(date)  and type='push_sdk' and country='%s'  union all select ad_id, 0 as impression, 0 as click, 0 as get_referrer, 0 as install, round(conversion* %s) as conversion, income* %s as income from native_report_daily_income_apk where  DATE_SUB(CURDATE(), INTERVAL %s DAY) = date(created_time) and is_valid='Y' ) t0 group by ad_id ) t1 left join native_ad t2 on t1.ad_id = t2.id  order by t1.install desc limit 120;"%(date_diff,country,ratio,ratio,date_diff)
    SQL_INFO(sql)
    return getSSPReportSlaveData(sql)



def loadPushSdkCountryFillratio(filename,startDate):
    data = getDailyCountryPushSdkData(startDate)
    dataDic = {str(a[0]).lower() : {'income':a[1],'dau':a[2]} for a in data}
    lines = []
    rows = []

    j = 0
    with open(filename) as fd:
        lines = fd.readlines()
            
    for line in lines:
        j += 1
        if j == 1:
            continue
        
        line=line.strip()
        if line == "":
            continue
        item = line.split('\t')

        data = []
        itemlen = len(item)

        data.append(str(j-1))
        if itemlen == 11:
            data.append('')

        for i in range(itemlen):
            data.append(item[i])

        adTotal = 0
        requestTotal = 0
        if itemlen == 11:
            adTotal = int(item[4]) + int(item[5])*2 + int(item[6])*3
            requestTotal = int(item[1])
        else:
            adTotal = int(item[5]) + int(item[6])*2 + int(item[7])*3
            requestTotal = int(item[2])
        
        ads_fill_average = round(float(adTotal)/float(requestTotal),2)
        data.append(ads_fill_average)

        country = item[0]
        if dataDic.has_key(country):
            income = dataDic[country]['income']
            dau = dataDic[country]['dau']
            dauIncome = round(float(income)/float(dau)*10000,2)

            data.append(income)
            data.append(dau)
            data.append(dauIncome)
        else:
            data.append('-')
            data.append('-')
            data.append('-')


        rows.append(data)

        #print ','.join(data)
    
    return rows

def saveNgpReport():
    db = DB.getSSPReportDb()
    sql = "select count(0) from native_report_ngp where date=unix_timestamp(utc_date())"
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    count = int(data[0]) if data != None else 0

    if count ==0:
        # sql = "select unix_timestamp(utc_date()),t1.ad_id,t2.advertiser_id,t1.country_code,t2.target_traffic_type,t2.bundle,1 from native_ngp_flags t1 left join native_ad t2 on t1.ad_id = t2.id where  t1.is_deleted=0 and t1.ngp=1 and t2.`status`=1 and t2.is_valid='Y'"
        sql = "select unix_timestamp(utc_date()),t1.ad_id,t2.advertiser_id,t1.country_code,t2.target_traffic_type,t2.bundle,1 from (select k3.ad_id,k3.country_code,1 as ngp,0 as is_deleted from ( select k1.ad_id,k1.country_code,k1.redirect_gp_market,if((select count(0) from native_offline_apk_data where ( status =1 or status=2 ) and errcode is null and bundle = k2.bundle)>0,1,0) as apk_downloaded from ( select ad_id,country_code,if(max(redirect_gp_market)>=3,max(redirect_gp_market)-3,max(redirect_gp_market)) redirect_gp_market from ( select ad_id,country_code,redirect_gp_market from native_ad_redirect_gp    union  all select ad_id,country_code,redirect_gp_market+3 from native_config_ad_redirect_gp where is_valid='Y' ) k group by ad_id,country_code ) k1 left join native_ad k2 on k1.ad_id = k2.id ) k3 where redirect_gp_market=1 and apk_downloaded=1) t1 left join native_ad t2 on t1.ad_id = t2.id where  t1.is_deleted=0 and t1.ngp=1 and t2.`status`=1 and t2.is_valid='Y'"
        SQL_INFO(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        resList = cursor.fetchall()

        for item in resList:
            sql = "insert into native_report_ngp(date,ad_id,union_id,country_code,target_traffic_type,bundle,ngp,created_by,status)values(%s,%s,%s,'%s',%s,'%s',%s,'ngp.report',1)"
            sql = sql%(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
            SQL_INFO(sql)
            cursor = db.cursor()
            cursor.execute(sql)

        db.commit()

    pass

def saveGuaranteePay():
    db = DB.getSSPReportDb()
    sql = "select  t2.app_id, t1.slot_id,  t3.user_id, t1.request, t1.impression, t1.click, t1.conversion, t1.dau, case when t1.conversion  =0 then 0 else t1.income end as income,DATE_FORMAT(date_sub(now(),interval 12 minute),'%Y-%m-%d') from ( select  slot_id,  request , request as impression , round(request * (0.15 + (RAND() * 0.1 - 0.05))) as click, round(request * (0.15 + (RAND() * 0.1 - 0.05)) * (0.015 + (RAND() * 0.01 - 0.005))) as conversion, dau, round((9.8 + (RAND()  - 0.5)) * (dau / 10000),3) as income from realtime_slot_report  where id in ( select max(id) from realtime_slot_report where log_date = DATE_FORMAT(date_sub(now(),interval 12 minute),'%Y-%m-%d') and product='np' and slot_id in (select id from ssp_slot where notes like '%Yeahmobi_PushSDK_1.2.0%') and slot_id not in (23587,810,23544,23545,23546) group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id left join ssp_app t3 on t2.app_id = t3.id "
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()

    for item in resList:
        sql = "insert into ssp_slot_report_guarantee_pay(app_id,slot_id,user_id,request,impression,click,conversion,dau,income,created_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')  ON DUPLICATE KEY UPDATE  request=case when request>%s then request else %s end, impression=case when impression>%s then impression else %s end, click=case when click>%s then click else %s end, conversion=case when conversion>%s then conversion else %s end, dau=case when dau>%s then dau else %s end, income=case when income>%s then income else %s end"
        sql = sql%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[3],item[3],item[4],item[4],item[5],item[5],item[6],item[6],item[7],item[7],item[8],item[8])
        SQL_INFO(sql)
        cursor = db.cursor()
        cursor.execute(sql)

    db.commit()

    pass

def saveGuaranteePay2(datestr):
    db = DB.getSSPReportDb()
    sql = "select  t2.app_id, t1.slot_id,  t3.user_id, t1.request, t1.impression, t1.click, t1.conversion, t1.dau, case when t1.conversion  =0 then 0 else t1.income end as income,'{0}' from ( select  slot_id,  request , request as impression , round(request * (0.15 + (RAND() * 0.1 - 0.05))) as click, round(request * (0.15 + (RAND() * 0.1 - 0.05)) * (0.015 + (RAND() * 0.01 - 0.005))) as conversion, dau, round((9.8 + (RAND()  - 0.5)) * (dau / 10000),3) as income from realtime_slot_report  where id in ( select max(id) from realtime_slot_report where log_date = '{1}' and product='np' and slot_id in (select id from ssp_slot where notes like '%Yeahmobi_PushSDK_1.2.0%') and slot_id not in (23587,810,23544,23545,23546) group by slot_id  ) ) t1 left join ssp_slot t2 on t1.slot_id = t2.id left join ssp_app t3 on t2.app_id = t3.id ".format(datestr, datestr)
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()

    for item in resList:
        sql = "insert into ssp_slot_report_guarantee_pay(app_id,slot_id,user_id,request,impression,click,conversion,dau,income,created_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s')  ON DUPLICATE KEY UPDATE  request=case when request>%s then request else %s end, impression=case when impression>%s then impression else %s end, click=case when click>%s then click else %s end, conversion=case when conversion>%s then conversion else %s end, dau=case when dau>%s then dau else %s end, income=case when income>%s then income else %s end"
        sql = sql%(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[3],item[3],item[4],item[4],item[5],item[5],item[6],item[6],item[7],item[7],item[8],item[8])
        SQL_INFO(sql)
        cursor = db.cursor()
        cursor.execute(sql)

    db.commit()

    pass



def saveSspSlotReportFinal(dateStr):
    db = DB.getSSPReportDb()
    sql = "delete from ssp_slot_report_final where created_time >='%s' and created_time<='%s'"
    sql = sql%(dateStr,dateStr)
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)

    sql = " insert into ssp_slot_report_final (app_id,slot_id,user_id,impression,click,conversion,dau,income,created_time)select t2.app_id,t2.slot_id,t2.user_id,case when t2.impression > ifnull(t3.impression,0) then t2.impression else ifnull(t3.impression,0) end impression,case when t2.click > ifnull(t3.click,0) then t2.click else ifnull(t3.click,0) end click,case when t2.conversion > ifnull(t3.conversion,0) then t2.conversion else ifnull(t3.conversion,0) end conversion,case when t2.dau > ifnull(t3.dau,0) then t2.dau else ifnull(t3.dau,0) end dau,case when t2.income > ifnull(t3.income,0) then t2.income else ifnull(t3.income,0) end income,'%s'from (    select app_id,slot_id,user_id,sum(impression) impression,sum(click) click,sum(conversion) conversion,sum(dau) dau,sum(income) income    from    (        SELECT a1.app_id,a1.slot_id,a1.user_id,a1.impression,a1.click,a1.conversion,ifnull(a2.dau,0) dau,a1.income,1 as type FROM ssp_slot_report a1         left join (select slot_id,dau from realtime_slot_report  where id in (                SELECT max(id)                FROM realtime_slot_report                WHERE log_date = '%s' and product='np' group by slot_id )        ) a2 on a1.slot_id = a2.slot_id  where a1.created_time >='%s' and a1.created_time<='%s'        union all        select k2.app_id,k1.slot_id,k3.user_id,0,0,0,0,0-withhold_amount,2 as type from native_finance_withhold_detail_daily k1 left join ssp_slot k2 on k1.slot_id = k2.id left join ssp_app k3 on k2.app_id = k3.id        where k1.status =1 and k1.withhold_time >='%s' and k1.withhold_time<='%s'    ) t1  group by app_id,slot_id,user_id) t2 left join (    SELECT app_id,slot_id,user_id,impression,click,conversion,dau,income FROM ssp_slot_report_guarantee_pay where created_time >='%s' and created_time<='%s') t3 on t2.app_id = t3.app_id and t2.slot_id = t3.slot_id and t2.user_id = t3.user_id;"
    sql = sql%(dateStr,dateStr,dateStr,dateStr,dateStr,dateStr,dateStr,dateStr)
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)

    db.commit()

    pass

def ReSaveSspSlotReportFinal():
    db = DB.getSSPReportDb()
    sql = "SELECT distinct(DATE_FORMAT(withhold_time,'%Y-%m-%d')) FROM native_finance_withhold_detail_daily where updated_time>= date_sub(curdate(),interval 1 hour)"
    SQL_INFO(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    resList = cursor.fetchall()

    for item in resList:
        saveSspSlotReportFinal(str(item[0]))

    pass

def checkSlotFillRate():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title = "Slot Fill Rate Below 0.8"
        columns = ['slot_id','requests','clicks','conversions','income','create_time','dau','ads_fill','ads_notfill','','fill_rate']
        data = getSlotFillRateLow()
        if len(data) > 0:
            html = gethtml(title,columns,data)
            #print html
            sendEmail(title,html)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="


def checkCountryFillRate():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title = "Country&TargetTrafficType Fill Rate Yesterday"

        title1 = 'Country Fill Rate Yesterday'
        columns = ['country','requests','clicks','conversions','ads_fill','ads_notfill','fill_rate']
        data = []
        data = data + list(getCountryRequestTop5())
        data = data + list(getCountryFillRateTop5())
        data = data + list(getCountryFillRateBottom5())
        data = data + list(getCountryFillRateAll())

        html = getTable(title1,columns,data)
        html += getTable("TargetTrafficType Fill Rate Yesterday","target_traffic_type,requests,clicks,conversions,ads_fill,ads_notfill,fill_rate".split(','),getTargetTrafficTypeFillRate())
        html += getTable("Slot Fill Rate Yesterday","slot_id,requests,clicks,conversions,ads_fill,ads_notfill,fill_rate".split(','),getSlotFillRateYesterday())
        
        cols = ['target_traffic_type']
        for i in range(1,8):
            name = getpreviousDate(i)
            cols.append(name)
        html += getTable("Fill Rate Last 7 Days",cols,getTargetTrafficTypeFillRateLast7day())

        cols[0] = 'slot_id'
        html += getTable("Slot Fill Rate Last 7 Days",cols,getSlotFillRateLast7day())

        if html != '':
            html = getHeader(html)
            sendEmail(title,html)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkDspUnapproved():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "DSP Ad & Creative Unapproved"

        html = getTable("Dsp Ad Unapproved","id,advertiser_id,ad_name,click_through_url,domain,updated_time".split(','),getDspAdUnapproved())
        html += getTable("Dsp Creative Unapproved","id,ad_id,ad_name,click_through_url,title,img_url,width,height,updated_time".split(','),getDspCreativeUnapproved(),{'img_url':'img'})
        
        if html != '':
            html = getHeader(html)
            to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="    

def checkNativeUnionStatus():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Native Union Status"

        html = getTable("Union Status","advertiser_name,last_import_time,last_updated_time,days_import_until_now,days_update_until_now,ad_count".split(','),getUnionStatus())

        if html != '':
            html = getHeader(html)
            #to = ["ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkNativeCreativeStatus():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Native Creative Status"

        html = getTable("Native ALL","size,creative count,ad count,bundle count".split(','),getNativeCreativeAll())
        html += getTable("Native NGP","size,creative count,ad count,bundle count".split(','),getNativeCreativeNGP())
        html += getTable("Push ALL","size,creative count,ad count,bundle count".split(','),getPushCreativeAll())
        html += getTable("Push NGP","size,creative count,ad count,bundle count".split(','),getPushCreativeNGP())

        if html != '':
            html = getHeader(html)
            #to = ["ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkPushNotificationStatus():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Push Notification Status"
        startDate = getpreviousDate(1)
        html = getTable("DATA 1","DAY,SLOT,VERSION,ECPM,收入/10000DAU,填充率,连wifi用户占比,人均返回广告数,下载成功率,CTR,安装成功率,确认率".split(','),getPushNotificationData1(startDate))
        html += getTable("DATA 2","DAY,SLOT,VERSION,请求广告DAU,全部请求数,有效广告请求数,填充率,服务端返回广告数,人均返回广告数".split(','),getPushNotificationData2(startDate))
        html += getTable("DATA 3","DAY,SLOT,VERSION,添加到下载队列广告数,下载开始DAU,连wifi用户占比,开始下载广告数,开始下载比率,下载成功广告数,人均下载次数,下载成功率".split(','),getPushNotificationData3(startDate))
        html += getTable("DATA 4","DAY,SLOT,VERSION,推送成功广告数,消息栏点击数,CTR,getreferrer成功广告数,getreferrer成功率,点击安装的广告数,用户选择安装比率,安装成功的广告数,安装成功率".split(','),getPushNotificationData4(startDate))
        html += getTable("DATA 5","DAY,SLOT,VERSION,添加到下载队列广告数,referrer发送成功数,referrer发送成功率,转化广告数,确认率,转化率".split(','),getPushNotificationData5(startDate))

        if html != '':
            html = getHeader(html)
            to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkPushNotificationDataForBD():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Push Notification Status For BD"
        startDate = getpreviousDate(1)

        data = getPushNotificationDataForBD(startDate)
        data += getPushNotificationDataForBDTotal(startDate)
        html = getTable("DATA 1","DAY,USER,CAMPANY,SLOT,ECPM,INCOME,AVERAGE CPI,DAU,收入/10000DAU,填充率,连wifi用户占比,人均返回广告数,下载成功率,CTR,安装成功率,确认率".split(','),data)

        if html != '':
            html = getHeader(html)
            #to = ["ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;judy.hu@yeahmobi.com;simon.lan@yeahmobi.com;daisy.wu@yeahmobi.com;frank.wang@yeahmobi.com;peter.zou@yeahmobi.com;dylan.zhuang@yeahmobi.com;peng.liu@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkPushSdkCountryFillratio():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Push Sdk Country FillRatio"
        for root, dirs, files in os.walk(PushSdkCountryFillratioFolder):
            for fn in files:
                filename = root + "/" + fn
                ext = os.path.splitext(filename)[1]
                if '.txt' != ext:
                    continue
                lastchange =datetime.datetime.fromtimestamp(os.path.getmtime(filename))
                starttime = datetime.datetime.now() - datetime.timedelta(minutes =10)
                # print '%s : %s => %s'%(filename,lastchange,starttime)
                startDate = getpreviousDate2(1)
                selector = startDate + '23.txt'
                #print selector
                if  selector in filename:
                    print filename
                    html = getTable("DATA 1(%s)"%filename,"id,country,day,total,ads_nofill,ads_fill,ads_fill_1,ads_fill_2,ads_fill_3,fill_rate,fill_with_1_ads,fill_with_2_ads,fill_with_3_ads,depth,income,dau,万Dau收入".split(','),loadPushSdkCountryFillratio(filename,startDate))
                    print html
                    if html != '':
                        html = getHeader(html)
                        #to = ["ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
                        to = ["displayads_tech@yeahmobi.com;displayads_pm@yeahmobi.com;native_ae@yeahmobi.com;judy.hu@yeahmobi.com;simon.lan@yeahmobi.com;dylan.zhuang@yeahmobi.com;daisy.wu@yeahmobi.com;yuanbin@yeahmobi.com;ping.zhang@yeahmobi.com;ulyx.yang@yeahmobi.com"]
                        sendEmail(title,html,to)

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="


def checkNgpReport():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        saveNgpReport()

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkGuaranteePay():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        saveGuaranteePay()

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkSspSlotReportFinal():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        dateStr = getpreviousDate(0)
        saveSspSlotReportFinal(dateStr)

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="


def get_date_str(date, offerset):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    d = date + datetime.timedelta(days=offerset)
    return d.strftime("%Y-%m-%d")

def checkSspSlotReportFinalForPeriod(argv):
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        start = argv[1]
        end = argv[2]
        i=0
        while(True):
            bizDate= get_date_str(start,i)
            print "======> bizDate: %s"%bizDate
            if(bizDate==end):
                break
            saveSspSlotReportFinal(bizDate)
            i=i+1

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def checkSspSlotReportFinalUpdate():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        ReSaveSspSlotReportFinal()

    except Exception as e:
        import traceback
        import StringIO
        fp = StringIO.StringIO()
        traceback.print_exc(file=fp)
        message = fp.getvalue()
        print "ERROR Happens Ingore",message
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="



def checkPushSlotAdConfirmRate():
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Push Sdk Top Offer"

        html = getTable("ALL","ad_id,unionname_offerid,bundle,cpa,imp,click,ctr,reffer,referrerRate,install,conversion,confirmRate,cvr,ecpm,income".split(','),getPushSlotAdConfirmRate())

        if html != '':
            html = getHeader(html)
            # to = ["ping.zhang@ndpmedia.com"]
            to = ["displayads_tech@ndpmedia.com;displayads_pm@ndpmedia.com;native_ae@ndpmedia.com;yuanbin@ndpmedia.com;ping.zhang@ndpmedia.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="


def checkPushSlotAdConfirmRateByCountry(country):
    print "==== The whole Process Start at " + time.ctime() + "===="

    try:
        title= "Push Sdk Top Offer By Country - %s"%(country.upper())

        html = getTable("ALL","ad_id,unionname_offerid,bundle,cpa,imp,click,ctr,reffer,referrerRate,install,conversion,confirmRate,cvr,ecpm,income".split(','),getPushSlotAdConfirmRateByCountry(country))

        if html != '':
            html = getHeader(html)
            #to = ["ping.zhang@ndpmedia.com"]
            to = ["displayads_tech@ndpmedia.com;displayads_pm@ndpmedia.com;native_ae@ndpmedia.com;yuanbin@ndpmedia.com;ping.zhang@ndpmedia.com;ulyx.yang@yeahmobi.com"]
            sendEmail(title,html,to)

    except Exception as e:
        print "ERROR Happens Ingore",e
        time.sleep(5)

    print "==== The whole Process End at " + time.ctime() + "===="

def run(op, argv):
    if op == 'checkSlotFillRate':
        checkSlotFillRate()
    elif op == 'checkCountryFillRate':
        checkCountryFillRate()
    elif op == 'checkDspUnapproved':
        checkDspUnapproved()
    elif op == 'checkNativeUnionStatus':
        checkNativeUnionStatus()
    elif op == 'checkNativeCreativeStatus':
        checkNativeCreativeStatus()
    elif op == 'checkNgpReport':
        checkNgpReport()
    elif op == 'checkPushNotificationStatus':
        checkPushNotificationStatus()
    elif op == 'checkPushNotificationDataForBD':
        checkPushNotificationDataForBD()
    elif op == 'checkPushSdkCountryFillratio':
        checkPushSdkCountryFillratio()
    elif op == 'checkGuaranteePay':
        checkGuaranteePay()
    elif op == 'checkSspSlotReportFinal':
        checkSspSlotReportFinal()
    elif op == 'checkSspSlotReportFinalUpdate':
        checkSspSlotReportFinalUpdate()
    elif op == 'checkSspSlotReportFinalForPeriod':
        checkSspSlotReportFinalForPeriod(argv)
    elif op == 'checkPushSlotAdConfirmRate':
        checkPushSlotAdConfirmRate()
    elif op == 'checkPushSlotAdConfirmRateByCountryIND':
        checkPushSlotAdConfirmRateByCountry('ind')
    elif op == 'checkPushSlotAdConfirmRateByCountryIDN':
        checkPushSlotAdConfirmRateByCountry('idn')        


def SQL_INFO(sql):
    print datetime.datetime.now(),"[SQL]", sql.encode('UTF-8')

def rerunGua(datestr):
    saveGuaranteePay2(datestr)
    saveSspSlotReportFinal(datestr)


def usage(msg):
    if msg != "":
        print "[ERROR]",msg
    print "Usage==============="
    print "python check_slot_fill_rate.py [TYPE]"
    print 'TIME_TYPE:',"checkSlotFillRate|checkCountryFillRate"
    print "===================="
    sys.exit()

if __name__ == "__main__":

    #rerunGua('2016-05-30')
    #sys.exit(1)

    argv = sys.argv[1:]

    if len(argv) < 1:
        usage("")

    op = argv[0]

    if op == 'checkSlotFillRate':       
        run(op, argv)
    elif op == 'checkCountryFillRate':       
        run(op, argv)
    elif op == 'checkDspUnapproved':
        run(op, argv)
    elif op == 'checkNativeUnionStatus':
        run(op, argv)
    elif op == 'checkNativeCreativeStatus':
        run(op, argv)
    elif op == 'checkNgpReport':
        run(op, argv)
    elif op == 'checkPushNotificationStatus':
        run(op, argv)
    elif op == 'checkPushNotificationDataForBD':
        run(op, argv)
    elif op == 'checkPushSdkCountryFillratio':
        run(op, argv)
    elif op == 'checkGuaranteePay':
        run(op, argv)
    elif op == 'checkSspSlotReportFinal':
        run(op, argv)
    elif op == 'checkSspSlotReportFinalUpdate':
        run(op, argv)
    elif op == 'checkSspSlotReportFinalForPeriod':
        run(op, argv)
    elif op == 'checkPushSlotAdConfirmRate':
        run(op, argv)
    elif op == 'checkPushSlotAdConfirmRateByCountryIND':
        run(op, argv)
    elif op == 'checkPushSlotAdConfirmRateByCountryIDN':
        run(op, argv)
    else:
        usage("Operation not supported "+op)  

    pass
