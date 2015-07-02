import os
import unittest

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class GprofLoaderTestCase(unittest.TestCase):
    def setUp(self):
        self.target = GprofLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'helloworld/gprof.callgraph.txt'
            ),
            False
        )

    def test_load_call_graph_errors(self):
        # Act
        graph = self.target.load_call_graph()

        # Assert
        self.assertEqual(0, len(self.target.errors))

    def test_load_call_graph_nodes(self):
        # Arrange
        expected = [
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C),
            Call('greet', './src/greetings.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('greet_b', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C)
        ]

        # Act
        graph = self.target.load_call_graph()
        actual = graph.nodes()
        match = (
            all([i in actual for i in expected]) and
            all([i in expected for i in actual])
        )

        # Assert
        self.assertCountEqual(expected, actual)
        for (_, attrs) in graph.nodes(data=True):
            self.assertTrue('tested' in attrs)
            self.assertTrue('defense' not in attrs)
            self.assertTrue('dangerous' not in attrs)
            self.assertTrue('vulnerable' not in attrs)

    def test_load_call_graph_entry_nodes(self):
        # Arrange
        expected = []

        # Act
        graph = self.target.load_call_graph()

        # Assert
        for (n, attrs) in graph.nodes(data=True):
            if n in expected:
                self.assertTrue('entry' in attrs)
            else:
                self.assertTrue('entry' not in attrs)

    def test_load_call_graph_exit_nodes(self):
        # Arrange
        expected = []

        # Act
        graph = self.target.load_call_graph()

        # Assert
        for (n, attrs) in graph.nodes(data=True):
            if n in expected:
                self.assertTrue('exit' in attrs)
            else:
                self.assertTrue('exit' not in attrs)

    def test_load_call_graph_edges(self):
        # Arrange
        expected = [
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ),
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ),
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ),
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ),
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ),
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
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
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ),
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('GreeterSayHi', './src/helloworld.c', Environments.C)
            ),
            (
                Call('GreeterSayHi', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ),
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C)
            ),
            (
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
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
                Call('greet_a', './src/helloworld.c', Environments.C)
            ),
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
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
                Call('main', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ),
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            )
        ]

        # Act
        graph = self.target.load_call_graph()
        actual = graph.edges()

        # Assert
        self.assertCountEqual(expected, actual)
        for (_, _, attrs) in graph.edges(data=True):
            self.assertTrue('gprof' in attrs)
            self.assertTrue('cflow' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_load_call_graph_return_edges(self):
        # Act
        graph = self.target.load_call_graph()

        # Assert
        self.assertTrue(nx.is_strongly_connected(graph))
        for (u, v) in nx.get_edge_attributes(graph, 'call'):
            self.assertTrue('return' in graph[v][u])

if __name__ == '__main__':
    unittest.main()
