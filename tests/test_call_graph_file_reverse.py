__author__ = 'kevin'

import unittest
import os
from tests.test_call_graph import CallGraphTestCase
from attacksurfacemeter import CallGraph


class CallGraphReverseFileTestCase(CallGraphTestCase):
    def setUp(self):
        self.call_graph = CallGraph(os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/callgraph.r.txt"), True)

if __name__ == '__main__':
    unittest.main()