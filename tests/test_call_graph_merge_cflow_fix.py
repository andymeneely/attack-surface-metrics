__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call import Call
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

    def test_nodes(self):
        # Arrange
        expected_content = [Call("malloc", "", "c"),
                            Call("scanf", "", "c"),
                            Call("GreeterSayHiTo", "./src/helloworld.c", "c"),
                            Call("functionPtr", "./src/helloworld.c", "c"),
                            Call("greet", "./src/greetings.c", "c"),
                            Call("recursive_a", "./src/greetings.c", "c"),
                            Call("greet_a", "./src/helloworld.c", "c"),
                            Call("addInt", "./src/helloworld.c", "c"),
                            Call("recursive_b", "./src/greetings.c", "c"),
                            Call("new_Greeter", "./src/helloworld.c", "c"),
                            Call("printf", "", "c"),
                            Call("greet_b", "./src/helloworld.c", "c"),
                            Call("GreeterSayHi", "helloworld.c", "c"),
                            Call("main", "./src/helloworld.c", "c"),
                            Call("puts", "", "c")]

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
        expected_content = [(Call("GreeterSayHi", "helloworld.c", "c"), Call("printf", "", "c")),
                            (Call("greet", "./src/greetings.c", "c"), Call("puts", "", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("malloc", "", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("GreeterSayHi", "helloworld.c", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
                            (Call("recursive_b", "./src/greetings.c", "c"), Call("recursive_a", "./src/greetings.c", "c")),
                            (Call("recursive_b", "./src/greetings.c", "c"), Call("printf", "", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("functionPtr", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("puts", "", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("greet_b", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("GreeterSayHi", "helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("new_Greeter", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("greet_a", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("printf", "", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("addInt", "./src/helloworld.c", "c")),
                            (Call("greet_b", "./src/helloworld.c", "c"), Call("greet", "./src/greetings.c", "c")),
                            (Call("greet_b", "./src/helloworld.c", "c"), Call("recursive_b", "./src/greetings.c", "c")),
                            (Call("greet_b", "./src/helloworld.c", "c"), Call("scanf", "", "c")),
                            (Call("recursive_a", "./src/greetings.c", "c"), Call("recursive_b", "./src/greetings.c", "c")),
                            (Call("recursive_a", "./src/greetings.c", "c"), Call("printf", "", "c")),
                            (Call("greet_a", "./src/helloworld.c", "c"), Call("greet", "./src/greetings.c", "c")),
                            (Call("greet_a", "./src/helloworld.c", "c"), Call("recursive_a", "./src/greetings.c", "c")),
                            (Call("GreeterSayHiTo", "./src/helloworld.c", "c"), Call("printf", "", "c"))]

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