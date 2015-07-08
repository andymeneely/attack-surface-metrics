import os
import statistics as stat

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.environments import Environments
from attacksurfacemeter.loaders.cflow_loader import CflowLoader


class BaseCflowTests(object):
    def test_nodes(self):
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
        actual = self.target.nodes

        # Assert
        self.assertCountEqual(expected, [i for (i, _) in actual])
        for (_, attrs) in actual:
            self.assertTrue('tested' not in attrs)
            self.assertFalse('defense' in attrs)
            self.assertFalse('dangerous' in attrs)
            self.assertFalse('vulnerable' in attrs)

    def test_entry_points(self):
        # Arrange
        expected = [
            Call('greet_b', './src/helloworld.c', Environments.C)
        ]

        # Act
        actual = self.target.entry_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_exit_points(self):
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
        actual = self.target.exit_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_edges(self):
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
        actual = self.target.edges

        # Assert
        self.assertCountEqual(expected, [(i, j) for (i, j, _) in actual])
        for (_, _, attrs) in actual:
            self.assertTrue('cflow' in attrs)
            self.assertTrue('gprof' not in attrs)
            self.assertTrue('call' in attrs or 'return' in attrs)

    def test_get_degree(self):
        # Arrange
        expected = {
            Call('main', './src/helloworld.c', Environments.C): (5, 5),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C): (1, 1),
            Call('new_Greeter', './src/helloworld.c', Environments.C): (3, 3),
            Call('greet', './src/greetings.c', Environments.C): (2, 2),
            Call('greet_b', './src/helloworld.c', Environments.C): (3, 3),
            Call('functionPtr', './src/helloworld.c', Environments.C): (1, 1),
            Call('recursive_b', './src/greetings.c', Environments.C): (2, 2),
            Call('addInt', './src/helloworld.c', Environments.C): (1, 1),
            Call('recursive_a', './src/greetings.c', Environments.C): (2, 2),
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C): 
                (1, 1),
            Call('greet_a', './src/helloworld.c', Environments.C): (3, 3)
        }

        # Act
        actual = self.target.get_degree()
        match = all([actual[i] == expected[i] for i in actual])

        # Assert
        self.assertEqual(len(expected), len(actual))
        self.assertTrue(match)

    def test_get_degree_of_call(self):
        # Arrange
        expected = (5, 5)

        # Act
        call = Call('main', './src/helloworld.c', Environments.C)
        actual = self.target.get_degree(call)

        # Assert
        self.assertEqual(expected, actual)

    def test_get_descendants(self):
        # Arrange
        expected = [
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('greet', './src/greetings.c', Environments.C),
            Call('functionPtr', './src/helloworld.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C)
        ]
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_descendants(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_ancestors(self):
        # Arrange
        expected = [
            Call('main', './src/helloworld.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C),
            Call('new_Greeter', './src/helloworld.c', Environments.C),
            Call('functionPtr', './src/helloworld.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('addInt', './src/helloworld.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('greet_a', './src/helloworld.c', Environments.C),
            Call('greet_b', './src/helloworld.c', Environments.C)
        ]
        call = Call('greet', './src/greetings.c', Environments.C)

        # Act
        actual = self.target.get_ancestors(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_nodes(self):
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

    def test_get_shortest_path_length_with_entry(self):
        # Arrange
        expected = {
            Call('greet_b', './src/helloworld.c', Environments.C): 2
        }
        call = Call('functionPtr', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_shortest_path_length(call, 'entry')

        # Assert
        self.assertCountEqual(expected, actual)
        self.assertAlmostEqual(
            stat.mean(expected.values()),
            stat.mean(expected.values()),
            places=4
        )

    def test_get_shortest_path_length_with_entry_for_entry(self):
        # Arrange
        expected = {}
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_shortest_path_length(call, 'entry')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_shortest_path_length_with_exit(self):
        # Arrange
        expected = {
            Call('greet', './src/greetings.c', Environments.C): 3,
            Call('recursive_a', './src/greetings.c', Environments.C): 3,
            Call('recursive_b', './src/greetings.c', Environments.C): 3,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C): 3,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C): 3,
            Call('main', './src/helloworld.c', Environments.C): 1
        }
        call = Call('functionPtr', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_shortest_path_length(call, 'exit')

        # Assert
        self.assertCountEqual(expected, actual)
        self.assertAlmostEqual(
            stat.mean(expected.values()),
            stat.mean(expected.values()), places=4
        )

    def test_get_shortest_path_length_with_exit_for_exit(self):
        # Arrange
        expected = {}
        call = Call('greet', './src/greetings.c', Environments.C)

        # Act
        actual = self.target.get_shortest_path_length(call, 'exit')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_entry_surface_metrics(self):
        # Arrange
        points = [Call('greet_b', './src/helloworld.c', Environments.C)]
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 1
            },
            Call('recursive_a', './src/greetings.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 1
            },
            Call('recursive_b', './src/greetings.c', Environments.C):
            {
                'points': points, 'proximity': 1.0, 'surface_coupling': 1
            },
            Call('new_Greeter', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 1
            },
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 3.0, 'surface_coupling': 1
            },
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 3.0, 'surface_coupling': 1
            },
            Call('main', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 1.0, 'surface_coupling': 1
            },
            Call('addInt', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 1
            },
            Call('greet_b', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('functionPtr', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 1
            },
            Call('greet', './src/greetings.c', Environments.C):
            {
                'points': points, 'proximity': 1.0, 'surface_coupling': 1
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
        points = [
            Call('greet', './src/greetings.c', Environments.C),
            Call('recursive_a', './src/greetings.c', Environments.C),
            Call('recursive_b', './src/greetings.c', Environments.C),
            Call('GreeterSayHi', './src/helloworld.c', Environments.C),
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
            Call('main', './src/helloworld.c', Environments.C)
        ]
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
            {
                'points': points,
                'proximity': 1.8333333333333333, 'surface_coupling': 6
            },
            Call('recursive_a', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('recursive_b', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('new_Greeter', './src/helloworld.c', Environments.C):
            {
                'points': points, 'proximity': 2.0, 'surface_coupling': 6
            },
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('main', './src/helloworld.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('addInt', './src/helloworld.c', Environments.C):
            {
                'points': points,
                'proximity': 2.6666666666666665, 'surface_coupling': 6
            },
            Call('greet_b', './src/helloworld.c', Environments.C):
            {
                'points': points,
                'proximity': 1.8333333333333333, 'surface_coupling': 6
            },
            Call('functionPtr', './src/helloworld.c', Environments.C):
            {
                'points': points,
                'proximity': 2.6666666666666665, 'surface_coupling': 6
            },
            Call('greet', './src/greetings.c', Environments.C):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
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
                0.10769946616084233,
            Call('main', './src/helloworld.c', Environments.C):
                0.17636263002647934,
            Call('greet', './src/greetings.c', Environments.C):
                0.08908839066792702,
            Call('addInt', './src/helloworld.c', Environments.C):
                0.029983385621464333,
            Call('greet_b', './src/helloworld.c', Environments.C):
                0.13110227632642915,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
                0.05772898265815536,
            Call('functionPtr', './src/helloworld.c', Environments.C):
                0.029983385621464333,
            Call('recursive_b', './src/greetings.c', Environments.C):
                0.09842707076406607,
            Call('recursive_a', './src/greetings.c', Environments.C):
                0.09377388044468546,
            Call('new_Greeter', './src/helloworld.c', Environments.C):
                0.12812154905033116,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
                0.05772898265815536
        }

        # Act
        actual = self.target.get_page_rank()

        # Assert
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertAlmostEqual(expected[i], actual[i])

    def test_get_page_rank_of_call(self):
        # Arrange
        expected = 0.13110227632642915
        call = Call('greet_b', './src/helloworld.c', Environments.C)

        # Act
        actual = self.target.get_page_rank(call)

        # Assert
        self.assertAlmostEqual(expected, actual)

    def test_assign_page_rank(self):
        # Arrange
        expected = {
            Call('greet_a', './src/helloworld.c', Environments.C):
                0.10769946616084233,
            Call('main', './src/helloworld.c', Environments.C):
                0.17636263002647934,
            Call('greet', './src/greetings.c', Environments.C):
                0.08908839066792702,
            Call('addInt', './src/helloworld.c', Environments.C):
                0.029983385621464333,
            Call('greet_b', './src/helloworld.c', Environments.C):
                0.13110227632642915,
            Call('GreeterSayHiTo', './src/helloworld.c', Environments.C):
                0.05772898265815536,
            Call('functionPtr', './src/helloworld.c', Environments.C):
                0.029983385621464333,
            Call('recursive_b', './src/greetings.c', Environments.C):
                0.09842707076406607,
            Call('recursive_a', './src/greetings.c', Environments.C):
                0.09377388044468546,
            Call('new_Greeter', './src/helloworld.c', Environments.C):
                0.12812154905033116,
            Call('GreeterSayHi', './src/helloworld.c', Environments.C):
                0.05772898265815536
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
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('GreeterSayHi', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('GreeterSayHi', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('new_Greeter', './src/helloworld.c', Environments.C),
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('GreeterSayHiTo', './src/helloworld.c', Environments.C),
                Call('new_Greeter', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('addInt', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('addInt', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('functionPtr', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('functionPtr', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('greet', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('greet', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('main', './src/helloworld.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 100,
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('main', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('greet_b', './src/helloworld.c', Environments.C),
                Call('recursive_b', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('recursive_b', './src/greetings.c', Environments.C),
                Call('greet_b', './src/helloworld.c', Environments.C)
            ): 50,
            (
                Call('greet_a', './src/helloworld.c', Environments.C),
                Call('recursive_a', './src/greetings.c', Environments.C)
            ): 100,
            (
                Call('recursive_a', './src/greetings.c', Environments.C),
                Call('greet_a', './src/helloworld.c', Environments.C)
            ): 50
        }

        # Act
        self.target.assign_weights()
        actual = nx.get_edge_attributes(self.target.call_graph, 'weight')

        # Assert
        self.assertCountEqual(expected, actual)
        for i in expected:
            self.assertEqual(expected[i], actual[i], msg=i)
