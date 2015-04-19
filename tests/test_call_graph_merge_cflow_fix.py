__author__ = 'kevin'

import unittest
import os

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader

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
        cflow_edges = set()
        gprof_edges = set()

        for edge in self.call_graph.edges:
            attributes = self.call_graph.call_graph.edge[edge[0]][edge[1]]
            if "cflow" in attributes:
                cflow_edges.add(edge)
            if "gprof" in attributes:
                gprof_edges.add(edge)

        # Edges tagged as 'cflow' only

        # Arrange
        expected_content = [
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

        cflow_only_edges = cflow_edges - gprof_edges

        # Assert
        self.assertEqual(12, len(cflow_only_edges))
        self.assertTrue(
            all([e in cflow_only_edges for e in expected_content])
        )
        for (u, v) in cflow_only_edges:
            self.assertEqual(1, 
                self.call_graph.call_graph.edge[u][v]['weight'])

        # Edges tagged as 'gprof' only

        # Arrange
        expected_content = [
            (Call("main", "./src/helloworld.c", "c"), 
                Call("GreeterSayHi", "./src/helloworld.c", "c")),
            (Call("main", "./src/helloworld.c", "c"), 
                Call("GreeterSayHiTo", "./src/helloworld.c", "c")),
        ]

        # Act
        gprof_only_edges = gprof_edges - cflow_edges

        # Assert
        self.assertEqual(2, len(gprof_only_edges))
        self.assertTrue(
            all([e in gprof_only_edges for e in expected_content])
        )
        for (u, v) in gprof_only_edges:
            self.assertEqual(0.5, 
                self.call_graph.call_graph.edge[u][v]['weight'])

        # Edges tagged as 'cflow' and 'gprof'

        # Arrange
        expected_content = [
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
        cflow_n_gprof_edges = cflow_edges & gprof_edges

        # Assert
        self.assertEqual(10, len(cflow_n_gprof_edges))
        self.assertTrue(
            all([e in cflow_n_gprof_edges for e in expected_content])
        )
        for (u, v) in gprof_only_edges:
            self.assertEqual(0.5, 
                self.call_graph.call_graph.edge[u][v]['weight'])

    def test_node_attributes(self):
        # Arrange
        expected_content = [
            Call("malloc", "", "c"),
            Call("scanf", "", "c"),
            Call("functionPtr", "./src/helloworld.c", "c"),
            Call("puts", "", "c"),
            Call("printf", "", "c")
        ]

        # Act
        untested_nodes = [
            node for node in self.call_graph.nodes 
                if not self.call_graph.call_graph.node[node]['tested']
        ]
        
        # Assert
        self.assertTrue(5, len(untested_nodes))
        self.assertTrue(all(n in untested_nodes for n in expected_content))

        # Arrange
        expected_content = [
            Call("recursive_a","./src/greetings.c","C"),
            Call("recursive_b","./src/greetings.c","C"),
            Call("greet_a","./src/helloworld.c","C"),
            Call("greet_b","./src/helloworld.c","C"),
            Call("greet","./src/greetings.c","C"),
            Call("main","./src/helloworld.c","C"),
            Call("new_Greeter","./src/helloworld.c","C"),
            Call("GreeterSayHiTo","./src/helloworld.c","C"),
            Call("addInt","./src/helloworld.c","C"),
            Call("GreeterSayHi","./src/helloworld.c","C"),
        ]

        # Act
        tested_nodes = [
            node for node in self.call_graph.nodes 
                if self.call_graph.call_graph.node[node]['tested']
        ]

        # Assert
        self.assertTrue(
            all(n in tested_nodes for n in expected_content)
        )


if __name__ == '__main__':
    unittest.main()
