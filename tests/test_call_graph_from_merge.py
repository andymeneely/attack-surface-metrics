import os
import unittest

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader
from tests.base_merge_tests import BaseMergeTests


class CallGraphFromMergeTestCase(unittest.TestCase, BaseMergeTests):
    def setUp(self):
        self.target = CallGraph.from_merge(
            CallGraph.from_loader(
                CflowLoader(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        'helloworld/cflow.callgraph.r.txt'
                    ),
                    True
                )
            ),
            CallGraph.from_loader(
                GprofLoader(
                    os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        'helloworld/gprof.callgraph.txt'
                    )
                )
            )
        )

if __name__ == '__main__':
    unittest.main()
