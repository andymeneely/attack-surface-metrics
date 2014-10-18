__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call import Call

from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader
from loaders.gprof_loader import GprofLoader


class CallGraphMergeTestCase(unittest.TestCase):
    def setUp(self):
        cflow_loader = CflowLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/cflow.callgraph.txt"),
            False)

        gprof_loader = GprofLoader(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/gprof.callgraph.txt"),
            False)

        cflow_call_graph = CallGraph.from_loader(cflow_loader)
        gprof_call_graph = CallGraph.from_loader(gprof_loader)

        self.call_graph = CallGraph.from_merge(cflow_call_graph, gprof_call_graph)

    def test_construction(self):
        pass

    def test_nodes(self):
        # Arrange
        expected_content = [Call("malloc", ""),
                            Call("scanf", ""),
                            Call("GreeterSayHiTo", "helloworld.c"),
                            Call("functionPtr", "helloworld.c"),
                            Call("greet", "greetings.c"),
                            Call("recursive_a", "greetings.c"),
                            Call("greet_a", "helloworld.c"),
                            Call("addInt", "helloworld.c"),
                            Call("recursive_b", "greetings.c"),
                            Call("new_Greeter", "helloworld.c"),
                            Call("printf", ""),
                            Call("greet_b", "helloworld.c"),
                            Call("GreeterSayHi", "helloworld.c"),
                            Call("main", "helloworld.c"),
                            Call("puts", "")]

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
        expected_content = [(Call("GreeterSayHi", "helloworld.c"), Call("printf", "")),
                            (Call("greet", "greetings.c"), Call("puts", "")),
                            (Call("new_Greeter", "helloworld.c"), Call("malloc", "")),
                            (Call("new_Greeter", "helloworld.c"), Call("GreeterSayHi", "helloworld.c")),
                            (Call("new_Greeter", "helloworld.c"), Call("GreeterSayHiTo", "helloworld.c")),
                            (Call("recursive_b", "greetings.c"), Call("recursive_a", "greetings.c")),
                            (Call("recursive_b", "greetings.c"), Call("printf", "")),
                            (Call("main", "helloworld.c"), Call("functionPtr", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("puts", "")),
                            (Call("main", "helloworld.c"), Call("greet_b", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("GreeterSayHi", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("new_Greeter", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("greet_a", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("GreeterSayHiTo", "helloworld.c")),
                            (Call("main", "helloworld.c"), Call("printf", "")),
                            (Call("main", "helloworld.c"), Call("addInt", "helloworld.c")),
                            (Call("greet_b", "helloworld.c"), Call("greet", "greetings.c")),
                            (Call("greet_b", "helloworld.c"), Call("recursive_b", "greetings.c")),
                            (Call("greet_b", "helloworld.c"), Call("scanf", "")),
                            (Call("recursive_a", "greetings.c"), Call("recursive_b", "greetings.c")),
                            (Call("recursive_a", "greetings.c"), Call("printf", "")),
                            (Call("greet_a", "helloworld.c"), Call("greet", "greetings.c")),
                            (Call("greet_a", "helloworld.c"), Call("recursive_a", "greetings.c")),
                            (Call("GreeterSayHiTo", "helloworld.c"), Call("printf", ""))]

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