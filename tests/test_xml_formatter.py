import os
import unittest

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.formatters.xml_formatter import XmlFormatter

from tests.test_txt_formatter import TxtFormatterTestCase


class XmlFormatterTestCase(TxtFormatterTestCase):
    def setUp(self):
        call_graph = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld'
                )
            )
        )

        self.formatter = XmlFormatter(call_graph)

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'helloworld/formatter.output.xml'
        )

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'helloworld/formatter.summary.xml'
        )

if __name__ == '__main__':
    unittest.main()
