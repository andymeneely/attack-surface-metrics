__author__ = 'kevin'

import re


class CflowLineParser():
    """"""
    _instance = None

    @staticmethod
    def get_instance():
        if CflowLineParser._instance is None:
            CflowLineParser._instance = CflowLineParser()

        return CflowLineParser._instance

    indent = "    "

    def __init__(self):
        self._function_info = ""
        self._function_name = ""
        self._function_signature = ""
        self._level = 0

    def load(self, cflow_line):
        split_line = cflow_line.split(CflowLineParser.indent)
        self._function_info = split_line[-1].strip()
        self._level = len(split_line) - 1

        # function name
        function_name = re.search(r"(\w+\(\))", self._function_info).group(0)
        self._function_name = function_name[:function_name.index('(')]

        # function signature
        match = re.search(r"(\w+\.c)", self._function_info)
        if match:
            self._function_signature = match.group(0)

    def get_function_name(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._function_name

    def get_function_signature(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._function_signature

    def get_level(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._level

    def get_function_info(self, cflow_line=None):
        self._load_if_new(cflow_line)
        return self._function_info

    def _load_if_new(self, cflow_line):
        if cflow_line is not None:
            self.load(cflow_line)