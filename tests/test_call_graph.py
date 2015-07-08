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

    def test_assign_weights_w_defaults(self):
        # Arrange
        target = CallGraph(
            source='/tmp', graph=self._build_graph(), load_errors=list(),
        )
        expected = {
            ('main', 'read'): 75,
            ('read', 'main'): 25,
            ('main', 'write'): 100,
            ('write', 'main'): 25,
            ('main', 'parse'): 100,
            ('parse', 'main'): 25,
            ('main', 'analyze'): 100,
            ('analyze', 'main'): 25,
            ('main', 'memalloc'): 100,
            ('memalloc', 'main'): 25,
            ('read', 'readfile'): 75,
            ('readfile', 'read'): 25,
            ('read', 'validate'): 50,
            ('validate', 'read'): 25,
            ('write', 'writefile'): 75,
            ('writefile', 'write'): 50,
            ('parse', 'parsefile'): 125,
            ('parsefile', 'parse'): 50,
            ('analyze', 'analyzefile'): 100,
            ('analyzefile', 'analyze'): 50
        }

        # Act
        target.assign_weights()
        actual = nx.get_edge_attributes(target.call_graph, 'weight')

        # Assert
        self.assertCountEqual(expected, actual)
        for i in expected:
            self.assertEqual(expected[i], actual[i], msg=i)

    def test_assign_weights_wo_defaults(self):
        # Arrange
        target = CallGraph(
            source='/tmp', graph=self._build_graph(), load_errors=list(),
        )
        weights = {
            "base": {"call": 125, "return": 75},
            "dangerous": 35,
            "defense": -30,
            "tested": -25,
            "vulnerable": 35
        }
        expected = {
            ('main', 'read'): 100,
            ('read', 'main'): 50,
            ('main', 'write'): 135,
            ('write', 'main'): 50,
            ('main', 'parse'): 125,
            ('parse', 'main'): 50,
            ('main', 'analyze'): 135,
            ('analyze', 'main'): 50,
            ('main', 'memalloc'): 140,
            ('memalloc', 'main'): 50,
            ('read', 'readfile'): 100,
            ('readfile', 'read'): 50,
            ('read', 'validate'): 70,
            ('validate', 'read'): 50,
            ('write', 'writefile'): 100,
            ('writefile', 'write'): 85,
            ('parse', 'parsefile'): 160,
            ('parsefile', 'parse'): 75,
            ('analyze', 'analyzefile'): 125,
            ('analyzefile', 'analyze'): 85
        }

        # Act
        target.assign_weights(weights)
        actual = nx.get_edge_attributes(target.call_graph, 'weight')

        # Assert
        self.assertCountEqual(expected, actual)
        for i in expected:
            self.assertEqual(expected[i], actual[i], msg=i)

    def _build_graph(self):
        #######################################################################
        #
        #                             main
        #                               |
        #     +--------------------+----+-----+-----------+------------+
        #     |                    |          |           |            |
        #   read--------+        write      parse      analyze     memalloc
        #     |         |          |          |           |
        #  readfile  validate   writefile  parsefile  analyzefile
        #
        #######################################################################

        graph = nx.DiGraph()
        graph.add_nodes_from([
            'main', 'read', 'write', 'parse', 'analyze', 'memalloc',
            'readfile', 'validate', 'writefile', 'parsefile', 'analyzefile'
        ])
        nx.set_node_attributes(
            graph, 'dangerous', {'memalloc': None, 'parsefile': None}
        )
        nx.set_node_attributes(
            graph, 'defense', {'validate': None, 'memalloc': None}
        )
        nx.set_node_attributes(
            graph, 'tested',
            {
                'main': None, 'read': None, 'write': None, 'analyze': None,
                'memalloc': None, 'readfile': None, 'validate': None,
                'writefile': None
            }
        )
        nx.set_node_attributes(
            graph, 'vulnerable',
            {'memalloc': None, 'write': None, 'analyze': None}
        )

        graph.add_edges_from([
            (
                'main', 'read',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'read', 'main',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'main', 'write',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'write', 'main',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'main', 'parse',
                {'cflow': None, 'call': None}
            ),
            (
                'parse', 'main',
                {'cflow': None, 'return': None}
            ),
            (
                'main', 'analyze',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'analyze', 'main',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'main', 'memalloc',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'memalloc', 'main',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'read', 'readfile',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'readfile', 'read',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'read', 'validate',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'validate', 'read',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'write', 'writefile',
                {'cflow': None, 'gprof': None, 'call': None}
            ),
            (
                'writefile', 'write',
                {'cflow': None, 'gprof': None, 'return': None}
            ),
            (
                'parse', 'parsefile',
                {'cflow': None, 'call': None}
            ),
            (
                'parsefile', 'parse',
                {'cflow': None, 'return': None}
            ),
            (
                'analyze', 'analyzefile',
                {'cflow': None, 'call': None}
            ),
            (
                'analyzefile', 'analyze',
                {'cflow': None, 'return': None}
            )
        ])

        return graph


if __name__ == '__main__':
    unittest.main()
