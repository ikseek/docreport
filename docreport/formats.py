import re
from xml.sax.saxutils import escape

HTML_TEMPLATE_HEADER = """
<html>
  <head>
    <title>Documentation state for {description}</title>
    <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
    <link rel="stylesheet" type="text/css"
          href="http://cdn.datatables.net/1.10.10/css/jquery.dataTables.css">
    <script src="http://cdn.datatables.net/1.10.10/js/jquery.dataTables.js">
    </script>
    <script type="text/javascript">
      $(document).ready(function (){{
        $('#data').DataTable( {{
          paging: false
        }});
      }});
    </script>
  </head>
  <body>
    <table id="data" class="display">
    <thead>
      <tr>
        <th>Type</th>
        <th>Area</th>
        <th>File name</th>
        <th>Change author</th>
        <th>Change date</th>
      </tr>
    </thead>
    <tbody>
"""

HTML_TEMPLATE_FOOTER = """
    </tbody>
    </table>
  </body>
</html>
"""

CSV_TEMPLATE = \
    "{type} ; {area} ; {file_name} ; {change_author} ; {change_date}"


def produce_csv(description, docfiles):
    for docfile in docfiles:
        yield CSV_TEMPLATE.format(**vars(docfile))


def produce_html(description, docfiles):
    yield HTML_TEMPLATE_HEADER.format(description=description)
    for docfile in docfiles:
        yield html_table_row(docfile)
    yield HTML_TEMPLATE_FOOTER


def html_table_row(docfile):
    values = (docfile.type, docfile.area, docfile.file_name,
              docfile.change_author, docfile.change_date)
    wrapped = ["<td>" + escape_add_spaces(value) + "</td>" for value in values]
    return "<tr>" + "".join(wrapped) + "</tr>"


def escape_add_spaces(text):
    escaped = escape(text)
    return re.sub(r'([:/]+)', r'\1&#8203;', escaped)
