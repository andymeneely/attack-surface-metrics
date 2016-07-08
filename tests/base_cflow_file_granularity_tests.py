import os
import statistics as stat

import networkx as nx

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.environments import Environments as Env
from attacksurfacemeter.granularity import Granularity as Gran
from attacksurfacemeter.loaders.cflow_loader import CflowLoader


class BaseCflowFileGranularityTests(object):
    def test_nodes(self):
        # Arrange
        expected = [
            Call('', './src/helloworld.c', Env.C, Gran.FILE),
            Call('', './src/greetings.c', Env.C, Gran.FILE),
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
            Call('', './src/helloworld.c', Env.C, Gran.FILE)
        ]

        # Act
        actual = self.target.entry_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_exit_points(self):
        # Arrange
        expected = [
            Call('', './src/greetings.c', Env.C, Gran.FILE),
            Call('', './src/helloworld.c', Env.C, Gran.FILE),
        ]

        # Act
        actual = self.target.exit_points

        # Assert
        self.assertCountEqual(expected, actual)

    def test_edges(self):
        # Arrange
        expected = [
            (
                Call('', './src/helloworld.c', Env.C, Gran.FILE),
                Call('', './src/helloworld.c', Env.C, Gran.FILE)
            ),
            (
                Call('', './src/helloworld.c', Env.C, Gran.FILE),
                Call('', './src/greetings.c', Env.C, Gran.FILE)
            ),
            (
                Call('', './src/greetings.c', Env.C, Gran.FILE),
                Call('', './src/helloworld.c', Env.C, Gran.FILE)
            ),
            (
                Call('', './src/greetings.c', Env.C, Gran.FILE),
                Call('', './src/greetings.c', Env.C, Gran.FILE)
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
            Call('', './src/helloworld.c', Env.C, Gran.FILE): (2, 2),
            Call('', './src/greetings.c', Env.C, Gran.FILE): (2, 2)
        }

        # Act
        actual = self.target.get_degree()
        match = all([actual[i] == expected[i] for i in actual])

        # Assert
        self.assertEqual(len(expected), len(actual))
        self.assertTrue(match)

    def test_get_degree_of_call(self):
        # Arrange
        expected = (2, 2)

        # Act
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)
        actual = self.target.get_degree(call)

        # Assert
        self.assertEqual(expected, actual)

    def test_get_fan(self):
        # Arrange
        expected = {
            Call('', './src/helloworld.c', Env.C, Gran.FILE): (1, 2),
            Call('', './src/greetings.c', Env.C, Gran.FILE): (2, 1)
        }

        # Act
        actual = self.target.get_fan()
        match = all([actual[i] == expected[i] for i in actual])

        # Assert
        self.assertEqual(len(expected), len(actual))
        self.assertTrue(match)

    def test_get_fan_of_call(self):
        # Arrange
        expected = (1, 2)
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_fan(call)

        # Assert
        self.assertEqual(expected, actual)

    def test_get_descendants(self):
        # Arrange
        expected = [
            Call('', './src/greetings.c', Env.C, Gran.FILE),
        ]
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_descendants(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_ancestors(self):
        # Arrange
        expected = [
            Call('', './src/helloworld.c', Env.C, Gran.FILE),
        ]
        call = Call('', './src/greetings.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_ancestors(call)

        # Assert
        self.assertCountEqual(expected, actual)

    def test_get_nodes(self):
        # Arrange
        expected = [
            Call('', './src/greetings.c', Env.C, Gran.FILE),
            Call('', './src/helloworld.c', Env.C, Gran.FILE),
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
        expected = 0.5
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_entry_point_reachability(call)

        # Assert
        self.assertAlmostEqual(expected, actual, places=4)

    def test_get_entry_point_reachability_non_entry(self):
        # Arrange
        call = Call('', './src/greetings.c', Env.C, Gran.FILE)

        # Assert
        self.assertRaises(
            Exception,
            self.target.get_entry_point_reachability,
            call
        )

    def test_exit_point_reachability(self):
        # Arrange
        expected = 0.5
        call = Call('', './src/greetings.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_exit_point_reachability(call)

        # Assert
        self.assertAlmostEqual(expected, actual, places=4)

    def test_get_shortest_path_length_with_entry(self):
        # Arrange
        expected = {
            Call('', './src/helloworld.c', Env.C, Gran.FILE): 1
        }
        call = Call('', './src/greetings.c', Env.C, Gran.FILE)

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
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_shortest_path_length(call, 'entry')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_shortest_path_length_with_exit_for_exit(self):
        # Arrange
        expected = {}
        call = Call('', './src/greetings.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_shortest_path_length(call, 'exit')

        # Assert
        self.assertEqual(expected, actual)

    def test_get_entry_surface_metrics(self):
        # Arrange
        points = [Call('', './src/helloworld.c', Env.C, Gran.FILE)]
        expected = {
            Call('', './src/helloworld.c', Env.C, Gran.FILE):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('', './src/greetings.c', Env.C, Gran.FILE):
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
        points = None
        expected = {
            Call('', './src/greetings.c', Env.C, Gran.FILE):
            {
                'points': None, 'proximity': 0.0, 'surface_coupling': None
            },
            Call('', './src/helloworld.c', Env.C, Gran.FILE):
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
            Call('', './src/helloworld.c', Env.C, Gran.FILE): 0.525,
            Call('', './src/greetings.c', Env.C, Gran.FILE): 0.475
        }

        # Act
        actual = self.target.get_page_rank()

        # Assert
        self.assertEqual(len(expected), len(actual))
        for i in expected:
            self.assertAlmostEqual(expected[i], actual[i])

    def test_get_page_rank_of_call(self):
        # Arrange
        expected = 0.525
        call = Call('', './src/helloworld.c', Env.C, Gran.FILE)

        # Act
        actual = self.target.get_page_rank(call)

        # Assert
        self.assertAlmostEqual(expected, actual)

    def test_assign_page_rank(self):
        # Arrange
        expected = {
            Call('', './src/helloworld.c', Env.C, Gran.FILE): 0.525,
            Call('', './src/greetings.c', Env.C, Gran.FILE): 0.475
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
                Call('', './src/helloworld.c', Env.C, Gran.FILE),
                Call('', './src/helloworld.c', Env.C, Gran.FILE)
            ): 100,
            (
                Call('', './src/helloworld.c', Env.C, Gran.FILE),
                Call('', './src/greetings.c', Env.C, Gran.FILE)
            ): 100,
            (
                Call('', './src/greetings.c', Env.C, Gran.FILE),
                Call('', './src/helloworld.c', Env.C, Gran.FILE)
            ): 50,
            (
                Call('', './src/greetings.c', Env.C, Gran.FILE),
                Call('', './src/greetings.c', Env.C, Gran.FILE)
            ): 100
        }

        # Act
        self.target.assign_weights()
        actual = nx.get_edge_attributes(self.target.call_graph, 'weight')

        # Assert
        self.assertCountEqual(expected, actual)
        for i in expected:
            self.assertEqual(expected[i], actual[i], msg=i)
