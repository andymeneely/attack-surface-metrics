__author__ = 'kevin'

import unittest
from tests.test_call_graph import CallGraphTestCase
from attacksurfacemeter import CallGraph


class CallGraphReverseTestCase(CallGraphTestCase):
    def setUp(self):
        self.call_graph = CallGraph("./helloworld", True)

if __name__ == '__main__':
    unittest.main()