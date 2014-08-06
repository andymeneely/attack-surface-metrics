__author__ = 'kevin'

import unittest
import os
from attacksurfacemeter import CallGraph
from formatters import JsonFormatter


class JsonFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.formatter = JsonFormatter(
            CallGraph(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "helloworld")))

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.json")

if __name__ == '__main__':
    unittest.main()