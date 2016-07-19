import copy
import os
import unittest

import networkx as nx

from attacksurfacemeter import utilities
from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class UtilitiesTestCase(unittest.TestCase):
    def test_fix(self):
        # Arrange
        target = CallGraph.from_loader(
            CflowLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/cflow.callgraph.r.mod.txt'
                ),
                True
            )
        )
        _target = copy.deepcopy(target)
        reference = CallGraph.from_loader(
            GprofLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/gprof.callgraph.txt'
                )
            )
        )
        expected = {
            'before': Call('GreeterSayHi', '', Environments.C),
            'after': Call('GreeterSayHi', './src/helloworld.c', Environments.C)
        }

        # Act
        utilities.fix(target, using=reference)
        actual = {
            'before':  next(
                i
                for (i, _) in _target.nodes
                if i.function_name == 'GreeterSayHi'
            ),
            'after':  next(
                i
                for (i, _) in target.nodes
                if i.function_name == 'GreeterSayHi'
            )
        }

        # Assert
        self.assertEqual(expected['before'], actual['before'])
        self.assertEqual(expected['after'], actual['after'])
        # Asserting if node attributes got carried over
        self.assertCountEqual(
            [
                attrs
                for (i, attrs) in _target.nodes
                if i == expected['before']
            ],
            [
                attrs
                for (i, attrs) in target.nodes
                if i == expected['after']
            ]
        )
        # Asserting if edge attributes got carried over
        self.assertCountEqual(
            [
                attrs
                for (i, j, attrs) in _target.edges
                if i == expected['before'] or j == expected['before']
            ],
            [
                attrs
                for (i, j, attrs) in target.edges
                if i == expected['after'] or j == expected['after']
            ],
        )
        # Asserting if OTHER nodes and their attributes got carried over
        self.assertCountEqual(
            [
                (i, attrs)
                for (i, attrs) in _target.nodes
                if i != expected['before']
            ],
            [
                (i, attrs)
                for (i, attrs) in target.nodes
                if i != expected['after']
            ]
        )
        # Asserting if OTHER edges and their attributes got carried over
        self.assertCountEqual(
            [
                (i, j, attrs)
                for (i, j, attrs) in _target.edges
                if i != expected['before'] and j != expected['before']
            ],
            [
                (i, j, attrs)
                for (i, j, attrs) in target.edges
                if i != expected['after'] and j != expected['after']
            ],
        )

    def test_get_fragments(self):
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

        expected = [None] * 4
        expected[0] = nx.DiGraph()
        expected[0].add_nodes_from(['a', 'b', 'c', 'd'])
        expected[0].add_edges_from([
           ('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'), ('c', 'd'),
           ('d', 'c'), ('d', 'a'), ('a', 'd')
        ])

        expected[1] = nx.DiGraph()
        expected[1].add_nodes_from(['e', 'f', 'g'])
        expected[1].add_edges_from(
            [('e', 'f'), ('f', 'e'), ('f', 'g'), ('g', 'f')]
        )

        expected[2] = nx.DiGraph()
        expected[2].add_nodes_from(['h', 'i'])
        expected[2].add_edges_from([('i', 'h'), ('h', 'i')])

        expected[3] = nx.DiGraph()
        expected[3].add_nodes_from(['j'])

        # Act
        actual = utilities.get_fragments(graph)
        actual.sort(key=lambda i: len(i.nodes()), reverse=True)

        # Assert
        self.assertEqual(len(expected), len(actual))
        for i in range(4):
            self.assertCountEqual(expected[i].nodes(), actual[i].nodes())
            self.assertCountEqual(expected[i].edges(), actual[i].edges())

    def test_get_fragments_for_undirected(self):
        # Arrange

        #   a -- b   e -- f -- g
        #   |    |
        #   |    |
        #   d -- c   h -- i  j
        graph = nx.Graph()
        graph.add_nodes_from(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        )
        graph.add_edges_from([
           ('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a'), ('e', 'f'),
           ('f', 'g'), ('h', 'i')
        ])

        # Assert
        self.assertRaises(Exception, utilities.get_fragments, graph)

    def test_get_largest_fragment(self):
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
        actual = utilities.get_largest_fragment(utilities.get_fragments(graph))

        # Assert
        self.assertCountEqual(expected.nodes(), actual.nodes())
        self.assertCountEqual(expected.edges(), actual.edges())

    def test_get_node_attrs(self):
        # Scenario: main -- printf (cflow)

        # Arrange
        source = 'cflow'
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('printf', '', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, list(), list()
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNone(callee_attrs)

        # Scenario: main -- printf (gprof)

        # Arrange
        source = 'gprof'
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('printf', '', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, list(), list()
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNone(callee_attrs)

        # Scenario: main -- None (gprof)

        # Arrange
        source = 'gprof'
        caller = Call('main', 'main.c', Environments.C)
        callee = None

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, list(), list()
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNone(callee_attrs)

        # Scenario: main -- validate* (cflow)
        #   * Designed defense

        # Arrange
        source = 'cflow'
        defenses = [Call('validate', 'utils.c', Environments.C)]
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('validate', 'utils.c', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, defenses, list()
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNotNone(callee_attrs)
        self.assertTrue('tested' not in callee_attrs)
        self.assertTrue('defense' in callee_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertEqual(callee_attrs['frequency'], 1)

        # Scenario: main -- validate* (cflow)
        #   * Vulnerable

        # Arrange
        source = 'cflow'
        vulnerabilities = [Call('validate', 'utils.c', Environments.C)]
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('validate', 'utils.c', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, list(), vulnerabilities
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in callee_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNotNone(callee_attrs)
        self.assertTrue('tested' not in callee_attrs)
        self.assertTrue('defense' not in callee_attrs)
        self.assertTrue('vulnerable' in callee_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertEqual(callee_attrs['frequency'], 1)

        # Scenario: main* -- validate+ (cflow)
        #   * Vulnerable
        #   + Designed defense and vulnerable

        # Arrange
        source = 'cflow'
        defenses = [Call('validate', 'utils.c', Environments.C)]
        vulnerabilities = [
            Call('main', 'main.c', Environments.C),
            Call('validate', 'utils.c', Environments.C)
        ]
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('validate', 'utils.c', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, defenses, vulnerabilities
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNotNone(callee_attrs)
        self.assertTrue('tested' not in callee_attrs)
        self.assertTrue('defense' in callee_attrs)
        self.assertTrue('vulnerable' in callee_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertEqual(callee_attrs['frequency'], 1)

        # Scenario: main* -- validate+ (cflow)
        #   * Designed defense
        #   + Designed defense and vulnerable

        # Arrange
        source = 'cflow'
        defenses = [
            Call('main', 'main.c', Environments.C),
            Call('validate', 'utils.c', Environments.C)
        ]
        vulnerabilities = [
            Call('main', 'main.c', Environments.C),
            Call('validate', 'utils.c', Environments.C)
        ]
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('validate', 'utils.c', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, defenses, vulnerabilities
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' in caller_attrs)
        self.assertTrue('vulnerable' in caller_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNotNone(callee_attrs)
        self.assertTrue('tested' not in callee_attrs)
        self.assertTrue('defense' in callee_attrs)
        self.assertTrue('vulnerable' in callee_attrs)
        self.assertTrue('dangerous' not in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertEqual(callee_attrs['frequency'], 1)

        # Scenario: main -- chown (cflow)

        # Arrange
        source = 'cflow'
        caller = Call('main', 'main.c', Environments.C)
        callee = Call('chown', '', Environments.C)

        # Act
        (caller_attrs, callee_attrs) = utilities.get_node_attrs(
            source, caller, callee, list(), list()
        )

        # Assert

        # Caller Attributes
        self.assertTrue('tested' not in caller_attrs)
        self.assertTrue('defense' not in caller_attrs)
        self.assertTrue('vulnerable' not in caller_attrs)
        self.assertTrue('dangerous' in caller_attrs)
        self.assertTrue('entry' not in caller_attrs)
        self.assertTrue('exit' not in caller_attrs)
        self.assertTrue('frequency' not in caller_attrs)

        # Callee Attributes
        self.assertIsNone(callee_attrs)

if __name__ == '__main__':
    unittest.main()
