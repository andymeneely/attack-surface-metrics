__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call import Call

from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


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
                            Call("GreeterSayHi", "./src/helloworld.c", "c"),
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
        expected_content = [(Call("GreeterSayHi", "./src/helloworld.c", "c"), Call("printf", "", "c")),
                            (Call("greet", "./src/greetings.c", "c"), Call("puts", "", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("malloc", "", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("GreeterSayHi", "./src/helloworld.c", "c")),
                            (Call("new_Greeter", "./src/helloworld.c", "c"), Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
                            (Call("recursive_b", "./src/greetings.c", "c"), Call("recursive_a", "./src/greetings.c", "c")),
                            (Call("recursive_b", "./src/greetings.c", "c"), Call("printf", "", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("functionPtr", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("puts", "", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("greet_b", "./src/helloworld.c", "c")),
                            (Call("main", "./src/helloworld.c", "c"), Call("GreeterSayHi", "./src/helloworld.c", "c")),
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

    def test_edge_attributes(self):
        # Arrange
        cflow_only_expected_content = [
            (Call("GreeterSayHi", "./src/helloworld.c", "c"), 
                Call("printf", "", "c")),
            (Call("greet", "./src/greetings.c", "c"), 
                Call("puts", "", "c")),
            (Call("new_Greeter", "./src/helloworld.c", "c"), 
                Call("malloc", "", "c")),
            (Call("new_Greeter", "./src/helloworld.c", "c"), 
                Call("GreeterSayHi", "./src/helloworld.c", "c")),
            (Call("new_Greeter", "./src/helloworld.c", "c"), 
                Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
            (Call("recursive_b", "./src/greetings.c", "c"), 
                Call("printf", "", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("functionPtr", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("puts", "", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("printf", "", "c")),
            (Call("greet_b", "./src/helloworld.c", "c"), 
                Call("scanf", "", "c")),
            (Call("recursive_a", "./src/greetings.c", "c"), 
                Call("printf", "", "c")),
            (Call("GreeterSayHiTo", "./src/helloworld.c", "c"), 
                Call("printf", "", "c"))
        ]

        gprof_only_expected_content = [
            (Call("main", "./src/helloworld.c", "c"), 
                Call("GreeterSayHi", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
        ]

        cflow_n_gprof_expected_content = [
            (Call("recursive_b", "./src/greetings.c", "c"), 
                Call("recursive_a", "./src/greetings.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("greet_b", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("new_Greeter", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("greet_a", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("addInt", "./src/helloworld.c", "c")),
            (Call("greet_b", "./src/helloworld.c", "c"), 
                Call("greet", "./src/greetings.c", "c")),
            (Call("greet_b", "./src/helloworld.c", "c"), 
                Call("recursive_b", "./src/greetings.c", "c")),
            (Call("recursive_a", "./src/greetings.c", "c"), 
                Call("recursive_b", "./src/greetings.c", "c")),
            (Call("greet_a", "./src/helloworld.c", "c"), 
                Call("greet", "./src/greetings.c", "c")),
            (Call("greet_a", "./src/helloworld.c", "c"), 
                Call("recursive_a", "./src/greetings.c", "c")),
        ]

        # Act

        # Aliasing to improve readability
        get_edge_data = self.call_graph.call_graph.get_edge_data

        cflow_only_edges = [edge for edge in self.call_graph.edges 
            if ('cflow' in get_edge_data(*edge) 
                and 'gprof' not in get_edge_data(*edge))]
        gprof_only_edges = [edge for edge in self.call_graph.edges 
            if ('gprof' in get_edge_data(*edge) and 
                'cflow' not in get_edge_data(*edge))]
        cflow_n_gprof_edges = [
            edge for edge in self.call_graph.edges 
            if all(k in get_edge_data(*edge) for k in ('cflow', 'gprof'))
        ]

        # Assert
        self.assertEqual(len(cflow_only_expected_content), 
            len(cflow_only_edges))
        self.assertTrue(
            all(
                [e in cflow_only_edges for e in cflow_only_expected_content]
            )
        )

        self.assertEqual(len(gprof_only_expected_content), 
            len(gprof_only_edges))
        self.assertTrue(
            all(
                [e in gprof_only_edges for e in gprof_only_expected_content]
            )
        )

        self.assertEqual(len(cflow_n_gprof_expected_content), 
            len(cflow_n_gprof_edges))
        self.assertTrue(
            all(
                [e in cflow_n_gprof_edges for e in cflow_n_gprof_expected_content]
            )
        )

if __name__ == '__main__':
    unittest.main()
