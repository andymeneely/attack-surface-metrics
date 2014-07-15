__author__ = 'kevin'

from formatters.base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(BaseFormatter, self).__init__(call_graph)
