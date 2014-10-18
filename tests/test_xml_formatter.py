__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader
from formatters.xml_formatter import XmlFormatter

from tests.test_txt_formatter import TxtFormatterTestCase


class XmlFormatterTestCase(TxtFormatterTestCase):

    def setUp(self):
        self.call_graph = CallGraph.from_loader(
            CflowLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld")))

        self.formatter = XmlFormatter(self.call_graph)

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.xml")

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.summary.xml")

if __name__ == '__main__':
    unittest.main()