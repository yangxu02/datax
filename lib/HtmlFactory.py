# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#cssheader = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head><style type='text/css'>table.gridtable {   font-family: verdana,arial,sans-serif;  font-size:11px; color:#333333;  border-width: 1px;  border-color: #666666;  border-collapse: collapse;table-layout:fixed;}table.gridtable th { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #dedede;width:200px;}table.gridtable td { border-width: 1px;  padding: 8px;   border-style: solid;    border-color: #666666;  background-color: #ffffff;width:200px;}</style></head><body>"
cssheader = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head></head><body>"

def gethtml(title, columns, data):
    global cssheader
    content = cssheader
    content += getTable(title, columns, data)
    content += "</body></html>"

    #print content

    return content


def getHeader(html):
    global cssheader
    content = cssheader
    content += html
    content += "</body></html>"

    return content


def getTable(title, columns, data, option=None):
    if data is None or len(data) == 0:
        return ''
    content = ''
    content += "<p><b>%s:</b></p>" % title
    #content += "<table class=\"gridtable\">"
    content += '<table cellspacing="0" cellpadding="5" border="1">'
    content += "<tr>%s</tr>" % (''.join(["<th>%s</th>" % str(name) for name in columns]))
    for row in data:
        rowdata = []
        for i, item in enumerate(list(row)):
            tdc = str(item)
            if option is not None and option.has_key(columns[i]):
                if option[columns[i]] == 'img':
                    tdc = "<img src='%s' />" % str(item)
            td = "<td>%s</td>\r\n" % tdc
            rowdata.append(td)
        content += "<tr>%s</tr>" % (''.join(rowdata))
        content += '\r\n'
    content += "</table>"
    #print content
    return content
