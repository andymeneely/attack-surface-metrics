__author__ = 'kevin'


from attacksurfacemeter.formatters.base_formatter import BaseFormatter


class HtmlFormatter(BaseFormatter):

    def __init__(self, call_graph):
        super(HtmlFormatter, self).__init__(call_graph)

    @property
    def template_file(self):
        return "template.html"

    @property
    def summary_template_file(self):
        return "summary_template.html"