import os
import unittest

import networkx as nx

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.granularity import Granularity
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from tests.base_cflow_tests import BaseCflowTests
from tests.base_cflow_file_granularity_tests import (
    BaseCflowFileGranularityTests
)


class CallGraphFromCflowFileTestCase(unittest.TestCase, BaseCflowTests):
    def setUp(self):
        self.target = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/cflow.callgraph.txt'
                ),
                False
            )
        )


class CallGraphFileGranularityFromCflowFileTestCase(
            unittest.TestCase, BaseCflowFileGranularityTests
        ):
    def setUp(self):
        self.target = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/cflow.callgraph.txt'
                ),
                False
            ),
            granularity=Granularity.FILE
        )

if __name__ == '__main__':
    unittest.main()
