import os
import unittest

import networkx as nx


from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.gprof_loader import GprofLoader
from tests.base_gprof_tests import BaseGprofTests


class CallGraphFromGprofTestCase(unittest.TestCase, BaseGprofTests):
    def setUp(self):
        self.target = CallGraph.from_loader(
            GprofLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/gprof.callgraph.txt'
                ),
                True
            )
        )

if __name__ == '__main__':
    unittest.main()
