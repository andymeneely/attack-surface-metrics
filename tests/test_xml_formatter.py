__author__ = 'kevin'

import unittest
import os
from attacksurfacemeter import CallGraph
from tests.test_txt_formatter import TxtFormatterTestCase
from formatters import XmlFormatter


class XmlFormatterTestCase(TxtFormatterTestCase):

    def setUp(self):
        self.formatter = XmlFormatter(CallGraph(os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld")))

if __name__ == '__main__':
    unittest.main()