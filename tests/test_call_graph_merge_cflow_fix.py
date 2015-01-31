__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader
from loaders.gprof_loader import GprofLoader

from tests.test_call_graph_merge import CallGraphMergeTestCase


class CallGraphMergeCflowFixTestCase(CallGraphMergeTestCase):
    def setUp(self):
        cflow_loader = CflowLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/cflow.callgraph.r.mod.txt"),
            True)

        gprof_loader = GprofLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/gprof.callgraph.txt"),
            False)

        cflow_call_graph = CallGraph.from_loader(cflow_loader)
        gprof_call_graph = CallGraph.from_loader(gprof_loader)

        self.call_graph = CallGraph.from_merge(cflow_call_graph, gprof_call_graph)

if __name__ == '__main__':
    unittest.main()