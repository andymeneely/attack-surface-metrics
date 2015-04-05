__author__ = 'kevin'

import re

from attacksurfacemeter.loaders.base_line_parser import BaseLineParser


class CflowLineParser(BaseLineParser):
    """"""
    _instance = None

    @staticmethod
    def get_instance(cflow_line=None):
        if CflowLineParser._instance is None:
            CflowLineParser._instance = CflowLineParser()

        CflowLineParser._instance.load(cflow_line)

        return CflowLineParser._instance

    indent = "    "

    def __init__(self):
        super(CflowLineParser, self).__init__()
        self._level = 0

    def load(self, cflow_line):
        self.__init__()

        split_line = cflow_line.split(CflowLineParser.indent)
        function_info = split_line[-1].strip()
        self._level = len(split_line) - 1

        function_name = re.search(r"(\w+\(\))", function_info).group(0)
        self._function_name = function_name[:function_name.index('(')]

        match = re.search(r"(?:at\s)(\..*)(?::\d+>)", function_info)
        if match:
            self._function_signature = match.group(1)

    def get_level(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._level

    def _load_if_new(self, cflow_line):
        if cflow_line is not None:
            self.load(cflow_line)
