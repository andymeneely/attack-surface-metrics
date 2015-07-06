import os
import unittest

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.formatters.txt_formatter import TxtFormatter
from tests.base_formatter_tests import BaseFormatterTests


class TxtFormatterTestCase(unittest.TestCase, BaseFormatterTests):
    def setUp(self):
        call_graph = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld'
                )
            )
        )

        self.formatter = TxtFormatter(call_graph)

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'helloworld/formatter.output.txt'
        )

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'helloworld/formatter.summary.txt'
        )


if __name__ == '__main__':
    unittest.main()
