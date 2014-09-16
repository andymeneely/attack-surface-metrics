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

    def test_edges(self):
        # Arrange
        expected_content = [(Call("recursive_a", ""), Call("printf", "")),
                            (Call("recursive_a", ""), Call("recursive_b", "")),
                            (Call("new_Greeter", "helloworld.c"), Call("GreeterSayHi", "helloworld.c")),
                            (Call("new_Greeter", "helloworld.c"), Call("malloc", "")),
                            (Call("new_Greeter", "helloworld.c"), Call("GreeterSayHiTo", "")),
                            (Call("recursive_b", ""), Call("printf", "")),
                            (Call("recursive_b", ""), Call("recursive_a", "")),
                            (Call("main", "helloworld.c"), Call("greet_a", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("GreeterSayHi", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("functionPtr", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("greet_b", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("puts", "")),
                            (Call("main", "helloworld.c"), Call("printf", "")),
                            (Call("main", "helloworld.c"), Call("new_Greeter", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("GreeterSayHiTo", "")),
                            (Call("main", "helloworld.c"), Call("addInt", "helloworld.c")),
                            (Call("GreeterSayHiTo", ""), Call("printf", "")),
                            (Call("greet", ""), Call("puts", "")),
                            (Call("greet_a", "helloworld.c"), Call("recursive_a", "")),
                            (Call("greet_a", "helloworld.c"), Call("greet", "")),
                            (Call("GreeterSayHi", "helloworld.c"), Call("printf", "")),
                            (Call("greet_b", "helloworld.c"), Call("recursive_b", "")),
                            (Call("greet_b", "helloworld.c"), Call("gets", "")),
                            (Call("greet_b", "helloworld.c"), Call("greet", ""))]

        # Act
        edges = self.call_graph.edges
        all_calls_found = all([c in edges for c in expected_content])

        # for e in edges:
        #     print('(Call("' + e[0].function_name + '", "' + (e[0].function_signature if e[0].function_signature else "") + '"), ' +
        #            'Call("' + e[1].function_name + '", "' + (e[1].function_signature if e[1].function_signature else "") + '")),')

        # Assert
        self.assertEqual(24, len(edges))
        self.assertTrue(all_calls_found)


if __name__ == '__main__':
    unittest.main()