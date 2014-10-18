__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from loaders.cflow_loader import CflowLoader


class CallGraphTestCase(unittest.TestCase):

    def setUp(self):
        self.call_graph = CallGraph.from_loader(
            CflowLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld")))

    def test_entry_points(self):
        # Arrange
        expected_count = 1
        expected_content = [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        entry_points_count = len(self.call_graph.entry_points)
        entry_points = self.call_graph.entry_points
        all_entry_points_encountered = all([c in entry_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, entry_points_count)
        self.assertTrue(all_entry_points_encountered)

    def test_exit_points(self):
        # Arrange
        expected_count = 6
        expected_content = [Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")]

        # Act
        exit_points_count = len(self.call_graph.exit_points)
        exit_points = self.call_graph.exit_points
        all_exit_points_encountered = all([c in exit_points for c in expected_content])

        # for c in exit_points:
        #     print('Call.from_cflow("' + c.function_info + '"),')

        # Assert
        self.assertEqual(expected_count, exit_points_count)
        self.assertTrue(all_exit_points_encountered)

    def test_shortest_path(self):
        # Arrange
        n1 = Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")
        n2 = Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")

        expected_content = [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")]

        # Act
        call_path = self.call_graph.shortest_path(n1, n2)
        all_calls_found = all([c in call_path for c in expected_content])

        # for c in call_path:
        #     print('Call.from_cflow("' + c.function_info + '"),')

        # Assert
        self.assertEqual(3, len(call_path))
        self.assertTrue(all_calls_found)

    def test_nodes(self):
        # Arrange
        expected_content = [Call.from_cflow("printf()"),
                            Call.from_cflow("puts()"),
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"),
                            Call.from_cflow("scanf()"),
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"),
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"),
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call.from_cflow("malloc()"),
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")]

        # Act
        nodes = self.call_graph.nodes
        all_calls_found = all([c in nodes for c in expected_content])

        # for c in nodes:
        #     print('Call.from_cflow("' + c.function_info + '"),')

        # Assert
        self.assertEqual(15, len(nodes))
        self.assertTrue(all_calls_found)

    def test_edges(self):
        # Arrange
        expected_content = [(Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), Call.from_cflow("printf()")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("printf()")),
                            (Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"), Call.from_cflow("puts()")),
                            (Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"), Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>: [see 3]")),
                            (Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"), Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R): [see 7]")),
                            (Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"), Call.from_cflow("scanf()")),
                            (Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (recursive: see 5) [see 5]")),
                            (Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), Call.from_cflow("printf()")),
                            (Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")),
                            (Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), Call.from_cflow("printf()")),
                            (Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"), Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")),
                            (Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"), Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")),
                            (Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:")),
                            (Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")),
                            (Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call.from_cflow("malloc()")),
                            (Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), Call.from_cflow("puts()")),
                            (Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), Call.from_cflow("printf()"))]

        # Act
        edges = self.call_graph.edges
        all_calls_found = all([c in edges for c in expected_content])

        # for e in edges:
        #     print('(Call.from_cflow("' + e[0].function_info + '"), Call.from_cflow("' + e[1].function_info + '")),')

        # Assert
        self.assertEqual(22, len(edges))
        self.assertTrue(all_calls_found)

    def test_execution_paths(self):
        # Arrange
        expected_content = [[Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                             Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")],
                            [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R): [see 7]")],
                            [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>: [see 3]")]]

        # Act
        paths = self.call_graph.execution_paths
        all_paths_found = all([p in paths for p in expected_content])

        # for p in paths:
        #     print("[")
        #     for c in p:
        #         print('Call.from_cflow("' + c.function_info + '"),')
        #     print("],")

        # Assert
        self.assertEqual(3, len(paths))
        self.assertTrue(all_paths_found)

    def test_avg_execution_path(self):
        # Act
        average = self.call_graph.avg_execution_path_length

        # Assert
        self.assertEqual(2.3333333333333335, average)

    def test_median_execution_path(self):
        # Act
        median = self.call_graph.median_execution_path_length

        # Assert
        self.assertEqual(2, median)

    def test_entry_clustering_coefficient(self):
        # Act
        coefficient = self.call_graph.entry_points_clustering

        # Assert
        self.assertEqual(0.0, coefficient)

    def test_exit_clustering_coefficient(self):
        # Act
        coefficient = self.call_graph.exit_points_clustering

        # Assert
        self.assertEqual(0.1111111111111111, coefficient)

    def test_execution_paths_for_call(self):
        # Arrange
        call = Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")

        expected_content = [[Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                             Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")]]

        # Act
        paths = self.call_graph.get_execution_paths_for(call)
        all_paths_found = all([p in paths for p in expected_content])
        call_in_all_paths = all([call in p for p in paths])

        # Assert
        self.assertEqual(1, len(paths))
        self.assertTrue(all_paths_found)
        self.assertTrue(call_in_all_paths)

    # def _arrange_test_distance(self):
    #     path = [p for p in self.call_graph.execution_paths if len(p) == 3][0]
    #     first_call = path[0]
    #     second_call = path[1]
    #     third_call = path[2]
    #
    #     return path, first_call, second_call, third_call

    def test_distance_to_entry_point(self):
        # Arrange
        # path, first_call, second_call, third_call = self._arrange_test_distance()

        path = [p for p in self.call_graph.execution_paths if len(p) == 3][0]
        first_call = path[0]
        second_call = path[1]
        third_call = path[2]

        # Act
        first_distance = self.call_graph.get_distance_to_entry_point(first_call, [path])
        second_distance = self.call_graph.get_distance_to_entry_point(second_call, [path])
        third_distance = self.call_graph.get_distance_to_entry_point(third_call, [path])

        # Assert
        self.assertEqual(0, first_distance[0]['distance'])
        self.assertEqual(1, second_distance[0]['distance'])
        self.assertEqual(2, third_distance[0]['distance'])

    def test_distance_to_exit_point(self):
        # Arrange
        path = [p for p in self.call_graph.execution_paths if len(p) == 3][0]
        first_call = path[0]
        second_call = path[1]
        third_call = path[2]

        # Act
        first_distance = self.call_graph.get_distance_to_exit_point(first_call, [path])
        second_distance = self.call_graph.get_distance_to_exit_point(second_call, [path])
        third_distance = self.call_graph.get_distance_to_exit_point(third_call, [path])

        # Assert
        self.assertEqual(2, first_distance[0]['distance'])
        self.assertEqual(1, second_distance[0]['distance'])
        self.assertEqual(0, third_distance[0]['distance'])

    def test_all_betweenness(self):
        # Arrange
        expected_content = {Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 0.008241758241758242,
                            Call.from_cflow("puts()"): 0.0,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.01098901098901099,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.016483516483516484,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0.0,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 0.013736263736263738,
                            Call.from_cflow("scanf()"): 0.0,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.01098901098901099,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.01098901098901099,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call.from_cflow("malloc()"): 0.0,
                            Call.from_cflow("printf()"): 0.0,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.0027472527472527475,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.0027472527472527475,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0}

        # Act
        betweennesses = self.call_graph.get_betweenness()

        # for call, betweenness in betweennesses.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(betweenness) + ',')

        all_values_correct = all([betweennesses[c] == expected_content[c] for c in betweennesses])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(betweennesses))

    def test_node_specific_betweenness(self):
        # Arrange
        expected_value = 0.016483516483516484
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        betweenness = self.call_graph.get_betweenness(call)

        # Assert
        self.assertEqual(expected_value, betweenness)

    def test_median_betweenness(self):
        # Arrange
        expected_value = 0.0027472527472527475

        # Act
        betweenness = self.call_graph.median_betweenness

        # Assert
        self.assertEqual(expected_value, betweenness)

    def test_average_betweenness(self):
        # Arrange
        expected_value = 0.005128205128205128

        # Act
        betweenness = self.call_graph.average_betweenness

        # Assert
        self.assertEqual(expected_value, betweenness)

    def test_all_closeness(self):
        # Arrange
        expected_content = {Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.22857142857142856,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285,
                            Call.from_cflow("malloc()"): 0.0,
                            Call.from_cflow("scanf()"): 0.0,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0.6666666666666666,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 0.2857142857142857,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.07142857142857142,
                            Call.from_cflow("printf()"): 0.0,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 0.22321428571428573,
                            Call.from_cflow("puts()"): 0.0}

        # Act
        closenesses = self.call_graph.get_closeness()

        # for call, closeness in closenesses.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(closeness) + ',')

        all_values_correct = all([closenesses[c] == expected_content[c] for c in closenesses])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(closenesses))

    def test_node_specific_closeness(self):
        # Arrange
        expected_value = 0.22857142857142856
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        closeness = self.call_graph.get_closeness(call)

        # Assert
        self.assertEqual(expected_value, closeness)

    def test_median_closeness(self):
        # Arrange
        expected_value = 0.07142857142857142

        # Act
        closeness = self.call_graph.median_closeness

        # Assert
        self.assertEqual(expected_value, closeness)

    def test_average_closeness(self):
        # Arrange
        expected_value = 0.12694444444444444

        # Act
        closeness = self.call_graph.average_closeness

        # Assert
        self.assertEqual(expected_value, closeness)

    def test_all_degree_centrality(self):
        # Arrange
        expected_content = {Call.from_cflow("puts()"): 0.14285714285714285,
                            Call.from_cflow("printf()"): 0.3571428571428571,
                            Call.from_cflow("malloc()"): 0.07142857142857142,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0.5,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.21428571428571427,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.14285714285714285,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 0.21428571428571427,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.2857142857142857,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 0.2857142857142857,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.07142857142857142,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.07142857142857142,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.2857142857142857,
                            Call.from_cflow("scanf()"): 0.07142857142857142,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.14285714285714285,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.2857142857142857}

        # Act
        degrees = self.call_graph.get_degree_centrality()

        # for call, degree_centrality in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(degree_centrality) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_degree_centrality(self):
        # Arrange
        expected_value = 0.21428571428571427

        # Act
        degree_centrality = self.call_graph.median_degree_centrality

        # Assert
        self.assertEqual(expected_value, degree_centrality)

    def test_average_degree_centrality(self):
        # Arrange
        expected_value = 0.20952380952380953

        # Act
        degree_centrality = self.call_graph.average_degree_centrality

        # Assert
        self.assertEqual(expected_value, degree_centrality)

    def test_all_in_degree_centrality(self):
        # Arrange
        expected_content = {Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.07142857142857142,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call.from_cflow("malloc()"): 0.07142857142857142,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 0.07142857142857142,
                            Call.from_cflow("scanf()"): 0.07142857142857142,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call.from_cflow("printf()"): 0.3571428571428571,
                            Call.from_cflow("puts()"): 0.14285714285714285,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.07142857142857142,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.14285714285714285,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 0.07142857142857142,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.07142857142857142,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0.0}

        # Act
        degrees = self.call_graph.get_in_degree_centrality()

        # for call, in_degree_centrality in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(in_degree_centrality) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_in_degree_centrality(self):
        # Arrange
        expected_value = 0.07142857142857142

        # Act
        in_degree_centrality = self.call_graph.median_in_degree_centrality

        # Assert
        self.assertEqual(expected_value, in_degree_centrality)

    def test_average_in_degree_centrality(self):
        # Arrange
        expected_value = 0.10476190476190476

        # Act
        in_degree_centrality = self.call_graph.average_in_degree_centrality

        # Assert
        self.assertEqual(expected_value, in_degree_centrality)

    def test_all_out_degree_centrality(self):
        # Arrange
        expected_content = {Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call.from_cflow("puts()"): 0.0,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.07142857142857142,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0.5,
                            Call.from_cflow("scanf()"): 0.0,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.21428571428571427,
                            Call.from_cflow("printf()"): 0.0,
                            Call.from_cflow("malloc()"): 0.0,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 0.14285714285714285,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 0.21428571428571427}

        # Act
        degrees = self.call_graph.get_out_degree_centrality()

        # for call, out_degree_centrality in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(out_degree_centrality) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_out_degree_centrality(self):
        # Arrange
        expected_value = 0.07142857142857142

        # Act
        out_degree_centrality = self.call_graph.median_out_degree_centrality

        # Assert
        self.assertEqual(expected_value, out_degree_centrality)

    def test_average_out_degree_centrality(self):
        # Arrange
        expected_value = 0.10476190476190476

        # Act
        out_degree_centrality = self.call_graph.average_out_degree_centrality

        # Assert
        self.assertEqual(expected_value, out_degree_centrality)

    def test_node_specific_degree_centrality(self):
        # Arrange
        expected_value = 0.2857142857142857
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_node_specific_in_degree_centrality(self):
        # Arrange
        expected_value = 0.07142857142857142
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_in_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_node_specific_out_degree_centrality(self):
        # Arrange
        expected_value = 0.21428571428571427
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_out_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_degree(self):
        # Arrange
        expected_content = {Call.from_cflow("puts():"): 2,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>"): 7,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 2,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 4,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 3,
                            Call.from_cflow("malloc():"): 1,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 4,
                            Call.from_cflow("printf():"): 5,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>:"): 1,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 4,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>:"): 1,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 4,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 2,
                            Call.from_cflow("scanf():"): 1,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 3}

        # Act
        degrees = self.call_graph.get_degree()

        # for call, degree in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(degree) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_degree(self):
        # Arrange
        expected_value = 3

        # Act
        degree = self.call_graph.median_degree

        # Assert
        self.assertEqual(expected_value, degree)

    def test_average_degree(self):
        # Arrange
        expected_value = 2.933333333333333

        # Act
        degree = self.call_graph.average_degree

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_in_degree(self):
        # Arrange
        expected_content = {Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 1,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 1,
                            Call.from_cflow("puts()"): 2,
                            Call.from_cflow("scanf()"): 1,
                            Call.from_cflow("malloc()"): 1,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 1,
                            Call.from_cflow("printf()"): 5,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 1,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 2,
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 0,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 2,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 1,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 1,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 2,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 1}

        # Act
        degrees = self.call_graph.get_in_degree()

        # for call, in_degree in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(in_degree) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_in_degree(self):
        # Arrange
        expected_value = 1

        # Act
        in_degree = self.call_graph.median_in_degree

        # Assert
        self.assertEqual(expected_value, in_degree)

    def test_average_in_degree(self):
        # Arrange
        expected_value = 1.4666666666666666

        # Act
        in_degree = self.call_graph.average_in_degree

        # Assert
        self.assertEqual(expected_value, in_degree)

    def test_all_out_degree(self):
        # Arrange
        expected_content = {Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"): 7,
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0,
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:87>:"): 2,
                            Call.from_cflow("printf()"): 0,
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 1,
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 3,
                            Call.from_cflow("puts()"): 0,
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:93>:"): 3,
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 1,
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 2,
                            Call.from_cflow("scanf()"): 0,
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 2,
                            Call.from_cflow("malloc()"): 0,
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 1,
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0}

        # Act
        degrees = self.call_graph.get_out_degree()

        # for call, out_degree in degrees.items():
        #     print('Call.from_cflow("' + call.function_info + '"): ' + str(out_degree) + ',')

        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])


        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_median_out_degree(self):
        # Arrange
        expected_value = 1

        # Act
        out_degree = self.call_graph.median_out_degree

        # Assert
        self.assertEqual(expected_value, out_degree)

    def test_average_out_degree(self):
        # Arrange
        expected_value = 1.4666666666666666

        # Act
        out_degree = self.call_graph.average_out_degree

        # Assert
        self.assertEqual(expected_value, out_degree)

    def test_node_specific_degree(self):
        # Arrange
        expected_value = 4
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_node_specific_in_degree(self):
        # Arrange
        expected_value = 1
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_in_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_node_specific_out_degree(self):
        # Arrange
        expected_value = 3
        call = Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_out_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_get_descendants(self):
        # Arrange
        expected_count = 5
        expected_content = [Call.from_cflow("printf():"),
                            Call.from_cflow("puts():"),
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("printf()"),
                            Call.from_cflow("puts()"),
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")]
        call = Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")

        # Act
        descendants = self.call_graph.get_descendants(call)
        all_descendants_found = all([c in descendants for c in expected_content])

        # for c in descendants:
        #     print('Call.from_cflow("' + c.function_info + '"),')

        # Assert
        self.assertEqual(expected_count, len(descendants))
        self.assertTrue(all_descendants_found)

    def test_get_ancestors(self):
        # Arrange
        expected_count = 1
        expected_content = [Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")]
        call = Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")

        # Act
        ancestors = self.call_graph.get_ancestors(call)
        all_ancestors_found = all([c in ancestors for c in expected_content])

        # for c in ancestors:
        #     print('Call.from_cflow("' + c.function_info + '"),')

        # Assert
        self.assertEqual(expected_count, len(ancestors))
        self.assertTrue(all_ancestors_found)

    def test_descendant_entry_points(self):
        # Arrange
        call = Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_count = 1
        expected_content = [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        descendant_entry_points = self.call_graph.get_descendant_entry_points(call)
        all_found = all([c in descendant_entry_points for c in expected_content])

        # [print(n.function_info) for n in self.call_graph.get_descendant_entry_points(call)]

        # Assert
        self.assertEqual(expected_count, len(descendant_entry_points))
        self.assertTrue(all_found)

    def test_descendant_exit_points(self):
        # Arrange
        call = Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_count = 5
        expected_content = [Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")]

        # Act
        descendant_exit_points = self.call_graph.get_descendant_exit_points(call)
        all_found = all([c in descendant_exit_points for c in expected_content])

        # [print('Call.from_cflow("' + n.function_info + '"),') for n in self.call_graph.get_descendant_exit_points(call)]

        # Assert
        self.assertEqual(expected_count, len(descendant_exit_points))
        self.assertTrue(all_found)

    def test_descendants_entry_point_ratio(self):
        # Arrange
        call = Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_value = 0.07142857142857142

        # Act
        ratio = self.call_graph.get_descendants_entry_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_descendants_exit_point_ratio(self):
        # Arrange
        call = Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_value = 0.35714285714285715

        # Act
        ratio = self.call_graph.get_descendants_exit_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_ancestor_entry_points(self):
        # Arrange
        call = Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")
        expected_count = 1
        expected_content = [Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        ancestor_entry_points = self.call_graph.get_ancestor_entry_points(call)
        all_found = all([c in ancestor_entry_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(ancestor_entry_points))
        self.assertTrue(all_found)

    def test_ancestor_exit_points(self):
        # Arrange
        call = Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")
        expected_count = 2
        expected_content = [Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:")]

        # Act
        ancestor_exit_points = self.call_graph.get_ancestor_exit_points(call)
        all_found = all([c in ancestor_exit_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(ancestor_exit_points))
        self.assertTrue(all_found)

    def test_ancestors_entry_point_ratio(self):
        # Arrange
        call = Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")
        expected_value = 0.3333333333333333

        # Act
        ratio = self.call_graph.get_ancestors_entry_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_ancestors_exit_point_ratio(self):
        # Arrange
        call = Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")
        expected_value = 0.5

        # Act
        ratio = self.call_graph.get_ancestors_exit_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

if __name__ == '__main__':
    unittest.main()