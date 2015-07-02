import os
import unittest

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.cflow_loader import CflowLoader


class CflowLoaderTestCase(unittest.TestCase):
    def setUp(self):
        self.test_loader = CflowLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'helloworld/cflow.callgraph.txt'
            ),
            False
        )

    def test_load_call_graph_errors(self):
        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        self.assertEqual(0, len(self.test_loader.errors))

    def test_load_call_graph_nodes(self):
        # Arrange
        expected = [
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C),
            Call('greet', './src/greetings.c', Environments.C),
            Call('functionPtr', './src/helloworld.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('greet_b', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C)
        ]

        # Act
        test_graph = self.test_loader.load_call_graph()
        nodes = [n for n in test_graph.nodes()]

        all_nodes_found = (
            all([n in nodes for n in expected]) and
            all([n in expected for n in nodes])
        )

        # Assert
        self.assertEqual(len(expected), len(nodes))
        self.assertTrue(all_nodes_found)
        for (n, attrs) in test_graph.nodes(data=True):
            self.assertTrue('tested' not in attrs)
            self.assertFalse('defense' in attrs)
            self.assertFalse('dangerous' in attrs)
            self.assertFalse('vulnerable' in attrs)

    def test_load_call_graph_entry_nodes(self):
        # Arrange
        expected = [
            Call('greet_b', './src/helloworld.c', Environments.C)
        ]

        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('entry' in attrs)
            else:
                self.assertTrue('entry' not in attrs)

    def test_load_call_graph_exit_nodes(self):
        # Arrange
        expected = [
            Call('greet', './src/greetings.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C),
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C)
        ]

        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('exit' in attrs)
            else:
                self.assertTrue('exit' not in attrs)

    def test_load_call_graph_edges(self):
        # Arrange
        expected = [
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('GreeterSayHi', './src/helloworld.c', Environments.C)
            ),
            (
                Call('GreeterSayHi', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ),
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C)
            ),
            (
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('addInt', './src/helloworld.c', Environments.C)
            ),
            (
                Call('addInt', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('functionPtr', './src/helloworld.c', Environments.C)
            ),
            (
                Call('functionPtr', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ),
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ),
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ),
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ),
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)  
            ),
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ),
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            )
        ]

        # Act
        test_graph = self.test_loader.load_call_graph()
        edges = test_graph.edges()

        all_edges_found = all([c in edges for c in expected])

        # Assert
        self.assertEqual(len(expected), len(edges))
        self.assertTrue(all_edges_found)
        for (u, v, attrs) in test_graph.edges(data=True):
            self.assertTrue('cflow' in attrs)
            self.assertTrue('gprof' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_load_call_graph_return_edges(self):
        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        call_edges = nx.get_edge_attributes(test_graph, 'call')

        self.assertTrue(nx.is_strongly_connected(test_graph))
        for (u, v) in call_edges:
            self.assertTrue('return' in test_graph[v][u])

if __name__ == '__main__':
    unittest.main()
