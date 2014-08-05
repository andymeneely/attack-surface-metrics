__author__ = 'kevin'

import unittest
import os
from attacksurfacemeter import CallGraph
from tests.test_txt_formatter import TxtFormatterTestCase
from formatters import HtmlFormatter


class HtmlFormatterTestCase(TxtFormatterTestCase):

    def setUp(self):
        self.formatter = HtmlFormatter(
            CallGraph(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "helloworld")))

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.html")

    def test_write_output(self):
        # Arrange
        expected_lines = [l for l in open(self.formatter_output_file)]

        # Act
        lines = self.formatter.write_output().splitlines(keepends=True)
        # all_lines_found = all([l in lines for l in expected_lines])

        # Assert
        self.assertEqual(len(expected_lines), len(lines))
        # TODO: need to find a way to correctly test the contents of this
        # self.assertTrue(all_lines_found)

if __name__ == '__main__':
    unittest.main()