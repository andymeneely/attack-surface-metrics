__author__ = 'kevin'

import unittest
from attacksurfacemeter import CallGraph
from tests.test_txt_formatter import TxtFormatterTestCase
from formatters import XmlFormatter


class XmlFormatterTestCase(TxtFormatterTestCase):

    def setUp(self):
        self.formatter = XmlFormatter(CallGraph("./helloworld"))

if __name__ == '__main__':
    unittest.main()