# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json

header = '''
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<link href="http://c3js.org/css/c3-b03125fa.css" media="screen" rel="stylesheet" type="text/css" />
<script src="http://c3js.org/js/d3-3.5.6.min-77adef17.js" type="text/javascript"></script>
<script src="http://c3js.org/js/c3.min-4c5bef8f.js" type="text/javascript"></script>
<style>
div.chart {{
    max-width: 960px;
    margin: auto;
    border: 1px solid #73AD21;
}}
</style>

</head><title>{title}</title><body>
'''

footer = '''
<script>
$(document).ready(function(){{
{content}
}});
</script>
'''

chartTmpl = '''
var chart{col} = c3.generate({{
    bindto: '#{col}',
    data: {{
        x: '{xcol}',
        xFormat: '%Y-%m-%d',
        columns: {data}
    }},
    axis: {{
        x: {{
            type: 'timeseries',
            tick: {{
                format: '%Y-%m-%d'
            }}
        }}
    }}
}});

'''

def getOneChart(xaix, column, chartData):
    return chartTmpl.format(xcol=xaix, col=column, data=json.dumps(chartData))


def getHtml(title, columns, data):
    content = header.format(title=title)
    c3Data = []
    i = 0
    for col in columns:
        cell = []
        cell.append(col)
        for row in data:
            cell.append(str(row[i]))
        c3Data.append(cell)
        i = i + 1
    i = 1
    chartContent = ""
    while i < len(columns):
        content += '<div class="chart" id="{chart}"></div>'.format(chart=columns[i])
        chartContent += getOneChart(columns[0], columns[i], [c3Data[0], c3Data[i]])
        i = i + 1
    content += footer.format(content=chartContent)
    content += "</body></html>"

    return content



if __name__ == "__main__":

    testData = [
        ["20160601","123", "456"],
        ["20160602","789", "100"],
        ["20160603","1123", "4156"],
        ["20160604","7189", "1100"]
    ]
    print getHtml("", ["date", "imp", "click"], testData)

