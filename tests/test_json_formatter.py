__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader
from formatters.json_formatter import JsonFormatter


class JsonFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.formatter = JsonFormatter(
            CallGraph(
                CflowLoader(
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld"))))

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.json")

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.summary.json")

if __name__ == '__main__':
    unittest.main()