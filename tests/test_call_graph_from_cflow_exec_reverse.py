import os
import unittest

import networkx as nx

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from tests.base_cflow_tests import BaseCflowTests


class CallGraphFromCflowExecReverseTestCase(unittest.TestCase, BaseCflowTests):
    def setUp(self):
        self.target = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld'
                ),
                True
            )
        )

if __name__ == '__main__':
    unittest.main()
