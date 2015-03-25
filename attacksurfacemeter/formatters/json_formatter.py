__author__ = 'kevin'

from attacksurfacemeter.formatters.base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    """
        Produces a json report with the attack surface metrics calculated by call_graph
        and prints it to console.
    """
    def __init__(self, call_graph):
        super(JsonFormatter, self).__init__(call_graph)

    @property
    def template_file(self):
        return "template.json"

    @property
    def summary_template_file(self):
        return "summary_template.json"