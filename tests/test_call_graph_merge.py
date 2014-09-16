__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter import CallGraph, Call
from loaders import CflowLoader
from loaders import GprofLoader


class CallGraphFileTestCase(unittest.TestCase):
    def setUp(self):
        cflow_loader = CflowLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/callgraph.txt"),
            False)

        gprof_loader = GprofLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/helloworld.stats"),
            False)

        cflow_call_graph = CallGraph.from_loader(cflow_loader)
        gprof_call_graph = CallGraph.from_loader(gprof_loader)

        self.call_graph = CallGraph.from_merge(cflow_call_graph, gprof_call_graph)

    def test_construction(self):
        pass

    def test_nodes(self):
        # Arrange
        expected_content = [Call("recursive_b", "greetings.c"),
                            Call("malloc", ""),
                            Call("greet_a", ""),
                            Call("printf", ""),
                            Call("recursive_a", "greetings.c"),
                            Call("GreeterSayHi", "helloworld.c"),
                            Call("addInt", "helloworld.c"),
                            Call("main", "helloworld.c"),
                            Call("GreeterSayHiTo", ""),
                            Call("new_Greeter", "helloworld.c"),
                            Call("puts", ""),
                            Call("gets", ""),
                            Call("greet_b", ""),
                            Call("functionPtr", "helloworld.c"),
                            Call("greet", "greetings.c")]

        # Act
        nodes = self.call_graph.nodes
        all_calls_found = all([c in nodes for c in expected_content])

        # for c in nodes:
        #     print('Call("' + c.function_name + '", "' +
        #           (c.function_signature if c.function_signature else "") + '"),')

        # Assert
        self.assertEqual(15, len(nodes))
        self.assertTrue(all_calls_found)


if __name__ == '__main__':
    unittest.main()