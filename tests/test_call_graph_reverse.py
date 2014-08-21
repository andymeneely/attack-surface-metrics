__author__ = 'kevin'

import unittest
import os
from tests.test_call_graph import CallGraphTestCase
from attacksurfacemeter import CallGraph, CflowLoader


class CallGraphReverseTestCase(CallGraphTestCase):
    def setUp(self):
        self.call_graph = CallGraph(
            CflowLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld"), True))

if __name__ == '__main__':
    unittest.main()