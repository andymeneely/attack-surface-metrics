__author__ = 'kevin'

import re

from loaders import BaseLineParser


class CflowLineParser(BaseLineParser):
    """"""
    indent = "    "

    def __init__(self):
        super(CflowLineParser, self).__init__()
        self._level = 0

    @staticmethod
    def get_instance():
        return CflowLineParser._lazy_load_instance(CflowLineParser)

    def load(self, cflow_line):
        split_line = cflow_line.split(CflowLineParser.indent)
        function_info = split_line[-1].strip()
        self._level = len(split_line) - 1

        function_name = re.search(r"(\w+\(\))", function_info).group(0)
        self._function_name = function_name[:function_name.index('(')]

        match = re.search(r"(\w+\.c)", function_info)
        if match:
            self._function_signature = match.group(0)

    def get_level(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._level

    def _load_if_new(self, cflow_line):
        if cflow_line is not None:
            self.load(cflow_line)