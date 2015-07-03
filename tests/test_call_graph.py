import copy
import unittest

import networkx as nx

from attacksurfacemeter.call_graph import CallGraph

class CallGraphTestCase(unittest.TestCase):
    def test_call_graph_wo_fragmentize(self):
        # Arrange

        #   a -- b   e -- f -- g
        #   |    |
        #   |    |
        #   d -- c   h -- i  j
        graph = nx.DiGraph()
        graph.add_nodes_from(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        )
        graph.add_edges_from([
           ('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'd'),
           ('d', 'c'), ('d', 'a'), ('a', 'd'), ('e', 'f'), ('f', 'e'),
           ('f', 'g'), ('g', 'f'), ('h', 'i'), ('i', 'h')
        ])
        expected = copy.deepcopy(graph)

        # Act
        actual = CallGraph(
            source='/tmp', graph=graph, load_errors=list(), fragmentize=False
        )

        # Assert
        self.assertIsNone(actual.num_fragments)
        self.assertIsNone(actual.monolithicity)
        self.assertCountEqual(expected.nodes(), [i for (i, _) in actual.nodes])
        self.assertCountEqual(
            expected.edges(), [(i, j) for (i, j, _) in actual.edges]
        )

    def test_call_graph_w_fragmentize(self):
        # Arrange

        #   a -- b   e -- f -- g
        #   |    |
        #   |    |
        #   d -- c   h -- i  j
        graph = nx.DiGraph()
        graph.add_nodes_from(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        )
        graph.add_edges_from([
           ('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'd'),
           ('d', 'c'), ('d', 'a'), ('a', 'd'), ('e', 'f'), ('f', 'e'),
           ('f', 'g'), ('g', 'f'), ('h', 'i'), ('i', 'h')
        ])
        expected = nx.DiGraph()
        expected.add_nodes_from(['a', 'b', 'c', 'd'])
        expected.add_edges_from([
           ('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'd'),
           ('d', 'c'), ('d', 'a'), ('a', 'd')
        ])

        # Act
        actual = CallGraph(
            source='/tmp', graph=graph, load_errors=list(), fragmentize=True
        )

        # Assert
        self.assertEqual(4, actual.num_fragments)
        self.assertEqual(0.4, actual.monolithicity)
        self.assertCountEqual(expected.nodes(), [i for (i, _) in actual.nodes])
        self.assertCountEqual(
            expected.edges(), [(i, j) for (i, j, _) in actual.edges]
        )

if __name__ == '__main__':
    unittest.main()
