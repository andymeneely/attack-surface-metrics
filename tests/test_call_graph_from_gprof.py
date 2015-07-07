import os
import unittest

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class CallGraphFromGprofTestCase(unittest.TestCase):
    def setUp(self):
        self.target = CallGraph.from_loader(
            GprofLoader(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'helloworld/gprof.callgraph.txt'
                ),
                True
            )
        )

    def test_nodes(self):
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
        actual = self.target.nodes

        # Assert
        self.assertCountEqual(expected, [i for (i, _) in actual])
        for (_, attrs) in actual:
            self.assertTrue('tested' in attrs)
            self.assertTrue('defense' not in attrs)
            self.assertTrue('dangerous' not in attrs)
            self.assertTrue('vulnerable' not in attrs)

    def test_entry_points(self):
        # Arrange
        expected = []

        # Act
        actual = self.target.entry_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_exit_points(self):
        # Arrange
        expected = []

        # Act
        actual = self.target.exit_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_edges(self):
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
        actual = self.target.edges

        # Assert
        self.assertCountEqual(expected, [(i, j) for (i, j, _) in actual])
        for (_, _, attrs) in actual:
            self.assertTrue('gprof' in attrs)
            self.assertTrue('cflow' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_get_degree(self):
        # Arrange
        expected = {
            Call('main', './src/helloworld.c', Environments.C): 12,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C): 2,
            Call('new_Greeter', './src/helloworld.c', Environments.C): 2,
            Call('greet', './src/greetings.c', Environments.C): 4,
            Call('greet_b', './src/helloworld.c', Environments.C): 6,
            Call('recursive_b', './src/greetings.c', Environments.C): 4,
            Call('addInt', './src/helloworld.c', Environments.C): 2,
            Call('recursive_a', './src/greetings.c', Environments.C): 4,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C): 2,
            Call('greet_a', './src/helloworld.c', Environments.C): 6
        }

        # Act
        actual = self.target.get_degree()
        match = all([actual[i] == expected[i] for i in actual])

        # Assert
        self.assertEqual(len(expected), len(actual))
        self.assertTrue(match)

    def test_get_degree_of_call(self):
        # Arrange
        expected = 12

        # Act
        call = Call('main', './src/helloworld.c', Environments.C)
        actual = self.target.get_degree(call)

        # Assert
        self.assertEqual(expected, actual)

    def test_get_descendants(self):
        # Arrange
        expected = [
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C),
            Call('greet', './src/greetings.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C)
        ]
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_descendants(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_ancestors(self):
        # Arrange
        expected = [
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('greet_b', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C)
        ]
        call = Call('greet', './src/greetings.c', Environments.C)

        # Act
        actual = self.target.get_ancestors(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_nodes(self):
        # Arrange
        expected = []

        # Act
        actual = self.target.get_nodes(attribute='exit')

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_nodes_invalid_attribute(self):
        # Arrange
        expected = []

        # Act
        actual = self.target.get_nodes(attribute='foo')

        # Assert
        self.assertCountEqual(expected, actual)

    @unittest.expectedFailure
    def test_get_entry_point_reachability(self):
        # Arrange
        expected = 0.9090909090909091
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_entry_point_reachability(call)

        # Assert
        self.assertAlmostEqual(expected, actual, places=4)

    def test_get_entry_point_reachability_non_entry(self):
        # Arrange
        call = Call('greet_a', './src/helloworld.c', Environments.C)

        # Assert
        self.assertRaises(
            Exception,
            self.target.get_entry_point_reachability,
            call
        )

    @unittest.expectedFailure
    def test_exit_point_reachability(self):
        # Arrange
        expected = 0.9090909090909091
        call = Call('greet', './src/greetings.c', Environments.C)

        # Act
        actual = self.target.get_exit_point_reachability(call)

        # Assert
        self.assertAlmostEqual(expected, actual, places=4)

    def test_exit_point_reachability_non_exit(self):
        # Arrange
        call = Call('greet_a', './src/helloworld.c', Environments.C)

        # Assert
        self.assertRaises(
            Exception,
            self.target.get_exit_point_reachability,
            call
        )

    def test_get_association_metrics_with_entry(self):
        # Arrange
        expected = {}
        call = Call('new_Greeter', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_association_metrics(call, 'entry')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_association_metrics_with_entry_for_entry(self):
        # Arrange
        expected = {}
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_association_metrics(call, 'entry')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_association_metrics_with_exit(self):
        # Arrange
        expected = {}
        call = Call('new_Greeter', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_association_metrics(call, 'exit')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_association_metrics_with_exit_for_exit(self):
        # Arrange
        expected = {}
        call = Call('greet', './src/greetings.c', Environments.C)

        # Act
        actual = self.target.get_association_metrics(call, 'exit')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_entry_surface_metrics(self):
        # Arrange
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('recursive_a', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('recursive_b', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('main', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('addInt', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('greet_b', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('functionPtr', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('greet', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            }
        }

        for i in expected:
            # Act
            actual = self.target.get_entry_surface_metrics(i)

            # Assert
            self.assertIsInstance(actual, dict)
            self.assertTrue('points' in actual)
            self.assertTrue('proximity' in actual)
            self.assertTrue('surface_coupling' in actual)
            if expected[i]['points'] is None:
                self.assertEqual(expected[i]['points'], actual['points'])
            else:
                self.assertCountEqual(expected[i]['points'], actual['points'])
            self.assertAlmostEqual(
                expected[i]['proximity'], actual['proximity'], places=4
            )
            self.assertEqual(
                expected[i]['surface_coupling'], actual['surface_coupling']
            )

    def test_get_exit_surface_metrics(self):
        # Arrange
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('recursive_a', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('recursive_b', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('main', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('addInt', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('greet_b', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('functionPtr', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            },
            Call('greet', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': None, 'surface_coupling': None
            }
        }

        for i in expected:
            # Act
            actual = self.target.get_exit_surface_metrics(i)

            # Assert
            self.assertIsInstance(actual, dict)
            self.assertTrue('points' in actual)
            self.assertTrue('proximity' in actual)
            self.assertTrue('surface_coupling' in actual)
            if expected[i]['points'] is None:
                self.assertEqual(expected[i]['points'], actual['points'])
            else:
                self.assertCountEqual(expected[i]['points'], actual['points'])
            self.assertEqual(expected[i]['proximity'], actual['proximity'])
            self.assertEqual(
                expected[i]['surface_coupling'], actual['surface_coupling']
            )

    def test_get_page_rank(self):
        # Arrange
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
                0.12789113913543346,
            Call('main', './src/helloworld.c', Environments.C):
                0.2671500027198321,
            Call('greet', './src/greetings.c', Environments.C):
                0.08747233694516567,
            Call('addInt', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('greet_b', './src/helloworld.c', Environments.C):
                0.12789113913543343,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('recursive_b', './src/greetings.c', Environments.C):
                0.0891061715241686,
            Call('recursive_a', './src/greetings.c', Environments.C):
                0.08910617152416858,
            Call('new_Greeter', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
                0.052845759753949534
        }

        # Act
        actual = self.target.get_page_rank()

        # Assert
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertAlmostEqual(expected[i], actual[i])

    def test_get_page_rank_of_call(self):
        # Arrange
        expected = 0.12789113913543343
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_page_rank(call)

        # Assert
        self.assertAlmostEqual(expected, actual)

    def test_assign_page_rank(self):
        # Arrange
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
                0.12789113913543346,
            Call('main', './src/helloworld.c', Environments.C):
                0.2671500027198321,
            Call('greet', './src/greetings.c', Environments.C):
                0.08747233694516567,
            Call('addInt', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('greet_b', './src/helloworld.c', Environments.C):
                0.12789113913543343,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('recursive_b', './src/greetings.c', Environments.C):
                0.0891061715241686,
            Call('recursive_a', './src/greetings.c', Environments.C):
                0.08910617152416858,
            Call('new_Greeter', './src/helloworld.c', Environments.C):
                0.052845759753949534,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
                0.052845759753949534
        }

        # Act
        self.target.assign_page_rank()
        actual = nx.get_node_attributes(
            self.target.call_graph, 'page_rank'
        )

        # Assert
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertAlmostEqual(expected[i], actual[i])

    def test_assign_weights(self):
        # Arrange
        expected = {
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ): 75,
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('GreeterSayHi', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('GreeterSayHi', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('addInt', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('addInt', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ): 75,
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 25
        }

        # Act
        self.target.assign_weights()
        actual = nx.get_edge_attributes(self.target.call_graph, 'weight')

        # Assert
        self.assertCountEqual(expected, actual)
        for i in expected:
            self.assertEqual(expected[i], actual[i], msg=i)

if __name__ == '__main__':
    unittest.main()
