# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

header = '''
<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html><head>
<link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">   
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
<link rel="stylesheet" href="http://cdn.datatables.net/1.10.2/css/jquery.dataTables.min.css"></style>
<script src="https://nightly.datatables.net/js/jquery.dataTables.js"></script>
<script src="https://nightly.datatables.net/buttons/js/dataTables.buttons.min.js"></script>
<script src="https://nightly.datatables.net/buttons/js/buttons.html5.min.js?2"></script>
<script src="https://nightly.datatables.net/buttons/js/buttons.flash.min.js"></script>
<meta charset=utf-8 />
</head><body>
<a href="/" class="btn pull-right btn-info btn-sm"> <span class="glyphicon glyphicon-home"></span> Home </a>
'''
# //<a href="#" class="export">Export Table data into Excel</a>

footer = '''
<script>
$(document).ready(function(){

    $('#table tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );
 
    // DataTable
    var table = $('#table').dataTable({
     dom: 'Bfrtip',
     buttons: [
        {
          extend: 'excel',
          text: 'Export to Excel',
          fieldSeparator: ',',
          footer: false,
          exportOptions: {
            orthogonal: 'filter',
          }
        }
     ],
    "lengthMenu": [[25, 50, 100, -1],[25, 50, 100, "All"]]
    });
 
 /*
    // Apply the search
    table.columns().every( function () {
        var that = this;
 
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );
    */


});
</script>
'''


def gethtml(title, columns, data):
    content = header
    content += '<div id="dvData">'
    content += getTable(title, columns, data)
    content += '</div>'
    content += footer
    content += "</body></html>"

    return content


def getHeader(html):
    content = header
    content += '<div id="dvData">'
    content += html
    content += '</div>'
    content += footer
    content += "</body></html>"

    return content


def getTable(title, columns, data, option=None):
    if data is None or len(data) == 0:
        return ''
    content = ''
    content += "</p>"
    content += '<p><h1>' + title + '</h1></p>'
    content += "<table id=\"table\" class=\"table table-striped\">"
    content += "<thead>"
    content += "<tr>%s</tr>" % (''.join(["<th>%s</th>" % str(name) for name in columns]))
    content += "</thead><tbody>"
    for row in data:
        rowdata = []
        for i, item in enumerate(list(row)):
            tdc = str(item)
            if option is not None and option.has_key(columns[i]):
                if option[columns[i]] == 'img':
                    tdc = "<img src='%s' />" % str(item)
            td = "<td>%s</td>" % tdc
            rowdata.append(td)
        content += "<tr>%s</tr>" % (''.join(rowdata))
    content += "</tbody></table>"
    return content
