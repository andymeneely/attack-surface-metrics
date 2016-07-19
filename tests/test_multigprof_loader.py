import unittest
import os

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.environments import Environments as Env
from attacksurfacemeter.granularity import Granularity as Gran
from attacksurfacemeter.loaders.multigprof_loader import MultigprofLoader


class MultigprofLoaderTestCase(unittest.TestCase):
    def setUp(self):
        sources = [
            'multigprof/multigprof.one.callgraph.txt',
            'multigprof/multigprof.two.callgraph.txt'
        ]
        sources = [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), source)
            for source in sources
        ]
        self.test_loader = MultigprofLoader(sources, False)

    def test_load_call_graph_errors(self):
        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        self.assertEqual(0, len(self.test_loader.errors))

    def test_load_call_graph_nodes(self):
        # Arrange
        expected = [
            Call('main', 'multigprof.c', Env.C),
            Call('fibonacci', 'multigprof.c', Env.C),
            Call('factorial', 'multigprof.c', Env.C)
        ]

        # Act
        test_graph = self.test_loader.load_call_graph()
        nodes = test_graph.nodes()

        all_nodes_found = (
            all([n in nodes for n in expected]) and
            all([n in expected for n in nodes])
        )

        # Assert
        self.assertEqual(len(expected), len(nodes))
        self.assertTrue(all_nodes_found)
        for (n, attrs) in test_graph.nodes(data=True):
            self.assertTrue('tested' in attrs)
            self.assertFalse('defense' in attrs)
            self.assertFalse('dangerous' in attrs)
            self.assertFalse('vulnerable' in attrs)

    def test_load_call_graph_nodes_file_granularity(self):
        # Arrange
        expected = [
            Call('', 'multigprof.c', Env.C, Gran.FILE),
        ]

        # Act
        test_graph = self.test_loader.load_call_graph(granularity=Gran.FILE)
        nodes = test_graph.nodes()

        all_nodes_found = (
            all([n in nodes for n in expected]) and
            all([n in expected for n in nodes])
        )

        # Assert
        self.assertEqual(len(expected), len(nodes))
        self.assertTrue(all_nodes_found)
        for (n, attrs) in test_graph.nodes(data=True):
            self.assertTrue('tested' in attrs)
            self.assertFalse('defense' in attrs)
            self.assertFalse('dangerous' in attrs)
            self.assertFalse('vulnerable' in attrs)

    def test_load_call_graph_entry_nodes(self):
        # Arrange
        expected = []

        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('entry' in attrs)
            else:
                self.assertTrue('entry' not in attrs)

    def test_load_call_graph_entry_nodes_file_granularity(self):
        # Arrange
        expected = []

        # Act
        test_graph = self.test_loader.load_call_graph(granularity=Gran.FILE)

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('entry' in attrs)
            else:
                self.assertTrue('entry' not in attrs)

    def test_load_call_graph_exit_nodes(self):
        # Arrange
        expected = []

        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('exit' in attrs)
            else:
                self.assertTrue('exit' not in attrs)

    def test_load_call_graph_exit_nodes_file_granularity(self):
        # Arrange
        expected = []

        # Act
        test_graph = self.test_loader.load_call_graph(granularity=Gran.FILE)

        # Assert
        for (n, attrs) in test_graph.nodes(data=True):
            if n in expected:
                self.assertTrue('exit' in attrs)
            else:
                self.assertTrue('exit' not in attrs)

    def test_load_call_graph_edges(self):
        # Act
        expected = [
            (
                Call('main', 'multigprof.c', Env.C),
                Call('factorial', 'multigprof.c', Env.C)
            ),
            (
                Call('factorial', 'multigprof.c', Env.C),
                Call('main', 'multigprof.c', Env.C)
            ),
            (
                Call('factorial', 'multigprof.c', Env.C),
                Call('factorial', 'multigprof.c', Env.C)
            ),
            (
                Call('main', 'multigprof.c', Env.C),
                Call('fibonacci', 'multigprof.c', Env.C)
            ),
            (
                Call('fibonacci', 'multigprof.c', Env.C),
                Call('main', 'multigprof.c', Env.C)
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
            self.assertTrue('gprof' in attrs)
            self.assertTrue('cflow' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_load_call_graph_edges_file_granularity(self):
        # Act
        expected = [
            (
                Call('', 'multigprof.c', Env.C, Gran.FILE),
                Call('', 'multigprof.c', Env.C, Gran.FILE)
            )
        ]

        # Act
        test_graph = self.test_loader.load_call_graph(granularity=Gran.FILE)
        edges = test_graph.edges()

        all_edges_found = all([c in edges for c in expected])

        # Assert
        self.assertEqual(len(expected), len(edges))
        self.assertTrue(all_edges_found)
        for (u, v, attrs) in test_graph.edges(data=True):
            self.assertTrue('gprof' in attrs)
            self.assertTrue('cflow' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_load_call_graph_return_edges(self):
        # Act
        test_graph = self.test_loader.load_call_graph()

        # Assert
        call_edges = nx.get_edge_attributes(test_graph, 'call')

        self.assertTrue(nx.is_strongly_connected(test_graph))
        for (u, v) in call_edges:
            self.assertTrue('return' in test_graph[v][u])

    def test_load_call_graph_return_edges_file_granularity(self):
        # Act
        test_graph = self.test_loader.load_call_graph(granularity=Gran.FILE)

        # Assert
        call_edges = nx.get_edge_attributes(test_graph, 'call')

        self.assertTrue(nx.is_strongly_connected(test_graph))
        for (u, v) in call_edges:
            self.assertTrue('return' in test_graph[v][u])

    def test_node_attr_frequency(self):
        # Arrange
        sources = [
            'multigprof/multigprof.one.callgraph.txt',
            'multigprof/multigprof.one.callgraph.txt'
        ]
        sources = [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), source)
            for source in sources
        ]
        self.test_loader = MultigprofLoader(sources, False)
        expected = {
            Call('factorial', 'multigprof.c', Env.C): 2
        }

        # Act
        test_graph = self.test_loader.load_call_graph()
        actual = nx.get_node_attributes(test_graph, 'frequency')

        # Assert
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
