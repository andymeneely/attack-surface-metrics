__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter import Call, CallGraph
from loaders import CflowLoader
from formatters import TxtFormatter


class TxtFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.formatter = TxtFormatter(
            CallGraph(
                CflowLoader(
                    os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld"))))

        self.formatter_output_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.output.txt")

        self.formatter_summary_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "helloworld/formatter.summary.txt")

    def test_write_output(self):
        # Arrange
        expected_lines = [l for l in open(self.formatter_output_file)]

        # Act
        lines = self.formatter.write_output().splitlines(keepends=True)
        # all_lines_found = all([l in lines for l in expected_lines])

        # Assert
        self.assertEqual(len(expected_lines), len(lines))
        # TODO: need to find a way to correctly test the contents of this
        # self.assertTrue(all_lines_found)

    def test_write_summary(self):
        # Arrange
        expected_lines = [l for l in open(self.formatter_summary_file)]

        # Act
        lines = self.formatter.write_summary().splitlines(keepends=True)
        # all_lines_found = all([l in lines for l in expected_lines])

        # Assert
        self.assertEqual(len(expected_lines), len(lines))
        # TODO: need to find a way to correctly test the contents of this
        # self.assertTrue(all_lines_found)

    def test_source_dir(self):
        # Arrange
        expected_value = os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld")

        # Act
        source = self.formatter.source

        # Assert
        self.assertEqual(expected_value, source)

    def test_nodes_count(self):
        # Arrange
        expected_value = "15"

        # Act
        nodes_count = self.formatter.nodes_count

        # Assert
        self.assertEqual(expected_value, nodes_count)

    def test_nodes(self):
        # Arrange
        expected_count = 15
        expected_content = [Call("printf()"),
                            Call("puts()"),
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"),
                            Call("gets()"),
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"),
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"),
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call("malloc()"),
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")]

        # Act
        nodes = self.formatter.nodes
        all_calls_found = all([c in nodes for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(nodes))
        self.assertTrue(all_calls_found)

    def test_edges_count(self):
        # Arrange
        expected_value = "22"

        # Act
        edges_count = self.formatter.edges_count

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_edges(self):
        # Arrange
        expected_count = 22
        expected_content = [(Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (recursive: see 5) [see 5]")),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), Call("printf()")),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), Call("puts()")),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R): [see 7]")),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>: [see 3]")),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), Call("gets()")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("printf()")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>")),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), Call("puts()")),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call("malloc()")),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:")),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), Call("printf()")),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), Call("printf()")),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), Call("printf()"))]

        # Act
        edges = self.formatter.edges
        all_calls_found = all([c in edges for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(edges))
        self.assertTrue(all_calls_found)

    def test_entry_points_count(self):
        # Arrange
        expected_value = "1"

        # Act
        edges_count = self.formatter.entry_points_count

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_entry_points(self):
        # Arrange
        expected_count = 1
        expected_content = [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        entry_points_count = len(self.formatter.entry_points)
        entry_points = self.formatter.entry_points
        all_entry_points_encountered = all([c in entry_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, entry_points_count)
        self.assertTrue(all_entry_points_encountered)

    def test_exit_points_count(self):
        # Arrange
        expected_value = "6"

        # Act
        edges_count = self.formatter.exit_points_count

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_exit_points(self):
        # Arrange
        expected_count = 6
        expected_content = [Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")]

        # Act
        exit_points_count = len(self.formatter.exit_points)
        exit_points = self.formatter.exit_points
        all_exit_points_encountered = all([c in exit_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, exit_points_count)
        self.assertTrue(all_exit_points_encountered)

    def test_execution_paths_count(self):
        # Arrange
        expected_value = "3"

        # Act
        edges_count = self.formatter.execution_paths_count

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_execution_paths(self):
        # Arrange
        expected_count = 3
        expected_content = [[Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                             Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")],
                            [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R): [see 7]")],
                            [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>: [see 3]")]]

        # Act
        paths = self.formatter.execution_paths
        all_paths_found = all([p in paths for p in expected_content])

        # Assert
        self.assertEqual(expected_count, len(paths))
        self.assertTrue(all_paths_found)

    def test_average_execution_paths_length(self):
        # Arrange
        expected_value = "2.3333333333333335"

        # Act
        edges_count = self.formatter.average_execution_path_length

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_median_execution_paths_length(self):
        # Arrange
        expected_value = "2"

        # Act
        edges_count = self.formatter.median_execution_path_length

        # Assert
        self.assertEqual(expected_value, edges_count)

    def test_all_closeness(self):
        # Arrange
        expected_count = 15
        expected_content = [(Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0.0),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 0.22857142857142856),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 0.14285714285714285),
                            (Call("gets()"), 0.0),
                            (Call("puts()"), 0.0),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 0.22321428571428573),
                            (Call("printf()"), 0.0),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 0.07142857142857142),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0.0),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0.6666666666666666),
                            (Call("malloc()"), 0.0),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 0.07142857142857142),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 0.2857142857142857),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 0.07142857142857142),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 0.14285714285714285)]

        # Act
        closenesses = self.formatter.get_closeness()
        all_values_correct = all([c in expected_content for c in closenesses])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(expected_count, len(closenesses))

    def test_node_specific_closeness(self):
        # Arrange
        expected_value = "0.22857142857142856"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        closeness = self.formatter.get_closeness(call)

        # Assert
        self.assertEqual(expected_value, closeness)

    def test_all_betweenness(self):
        # Arrange
        expected_content = [(Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0.0),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 0.016483516483516484),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 0.01098901098901099),
                            (Call("gets()"), 0.0),
                            (Call("puts()"), 0.0),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 0.008241758241758242),
                            (Call("printf()"), 0.0),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 0.0027472527472527475),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0.0),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0.0),
                            (Call("malloc()"), 0.0),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 0.01098901098901099),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 0.013736263736263738),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 0.0027472527472527475),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 0.01098901098901099)]

        # Act
        betweennesses = self.formatter.get_betweenness()
        all_values_correct = all([c in expected_content for c in betweennesses])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(betweennesses))

    def test_node_specific_betweenness(self):
        # Arrange
        expected_value = "0.016483516483516484"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        betweenness = self.formatter.get_betweenness(call)

        # Assert
        self.assertEqual(expected_value, betweenness)

    def test_entry_point_clustering(self):
        # Arrange
        expected_value = "0.0"

        # Act
        entry_point_clustering = self.formatter.entry_points_clustering

        # Assert
        self.assertEqual(expected_value, entry_point_clustering)

    def test_exit_point_clustering(self):
        # Arrange
        expected_value = "0.1111111111111111"

        # Act
        exit_point_clustering = self.formatter.exit_points_clustering

        # Assert
        self.assertEqual(expected_value, exit_point_clustering)

    def test_all_degree_centrality(self):
        # Arrange
        expected_content = [(Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 0.21428571428571427),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 0.2857142857142857),
                            (Call("puts()"), 0.14285714285714285),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 0.2857142857142857),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 0.21428571428571427),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 0.14285714285714285),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0.5),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0.07142857142857142),
                            (Call("printf()"), 0.3571428571428571),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 0.2857142857142857),
                            (Call("gets()"), 0.07142857142857142),
                            (Call("malloc()"), 0.07142857142857142),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 0.2857142857142857),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 0.14285714285714285),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0.07142857142857142)]

        # Act
        degrees = self.formatter.get_degree_centrality()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_degree_centrality(self):
        # Arrange
        expected_value = "0.2857142857142857"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_in_degree_centrality(self):
        # Arrange
        expected_content = [(Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 0.14285714285714285),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 0.07142857142857142),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 0.07142857142857142),
                            (Call("puts()"), 0.14285714285714285),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 0.14285714285714285),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 0.07142857142857142),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 0.07142857142857142),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0.07142857142857142),
                            (Call("gets()"), 0.07142857142857142),
                            (Call("printf()"), 0.3571428571428571),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 0.14285714285714285),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 0.07142857142857142),
                            (Call("malloc()"), 0.07142857142857142),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0.07142857142857142),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0.0)]

        # Act
        degrees = self.formatter.get_in_degree_centrality()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_in_degree_centrality(self):
        # Arrange
        expected_value = "0.07142857142857142"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_in_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_out_degree_centrality(self):
        # Arrange
        expected_content = [(Call("malloc()"), 0.0),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 0.21428571428571427),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 0.14285714285714285),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 0.07142857142857142),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 0.21428571428571427),
                            (Call("puts()"), 0.0),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0.0),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0.0),
                            (Call("gets()"), 0.0),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 0.14285714285714285),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 0.07142857142857142),
                            (Call("printf()"), 0.0),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0.5),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 0.14285714285714285),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 0.07142857142857142)]

        # Act
        degrees = self.formatter.get_out_degree_centrality()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_out_degree_centrality(self):
        # Arrange
        expected_value = "0.21428571428571427"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_out_degree_centrality(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_degree(self):
        # Arrange
        expected_content = [(Call("malloc()"), 1),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 4),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 3),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 2),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 4),
                            (Call("puts()"), 2),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 1),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 1),
                            (Call("gets()"), 1),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 4),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 2),
                            (Call("printf()"), 5),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 7),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 4),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 3)]
        # Act
        degrees = self.formatter.get_degree()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_degree(self):
        # Arrange
        expected_value = "4"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_in_degree(self):
        # Arrange
        expected_content = [(Call("malloc()"), 1),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 1),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 1),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 1),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 1),
                            (Call("puts()"), 2),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 1),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 1),
                            (Call("gets()"), 1),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 2),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 1),
                            (Call("printf()"), 5),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 0),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 2),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 2)]

        # Act
        degrees = self.formatter.get_in_degree()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_in_degree(self):
        # Arrange
        expected_value = "1"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_in_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_all_out_degree(self):
        # Arrange
        expected_content = [(Call("malloc()"), 0),
                            (Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"), 3),
                            (Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"), 2),
                            (Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"), 1),
                            (Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"), 3),
                            (Call("puts()"), 0),
                            (Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"), 0),
                            (Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"), 0),
                            (Call("gets()"), 0),
                            (Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"), 2),
                            (Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"), 1),
                            (Call("printf()"), 0),
                            (Call("main() <int main (void) at ./src/helloworld.c:58>:"), 7),
                            (Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"), 2),
                            (Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"), 1)]
        # Act
        degrees = self.formatter.get_out_degree()
        all_values_correct = all([c in expected_content for c in degrees])

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(15, len(degrees))

    def test_node_specific_out_degree(self):
        # Arrange
        expected_value = "3"
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.formatter.get_out_degree(call)

        # Assert
        self.assertEqual(expected_value, degree)

    def test_descendant_entry_points(self):
        # Arrange
        call = Call("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_count = 1
        expected_content = [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        descendant_entry_points = self.formatter.get_descendant_entry_points(call)
        all_found = all([c in descendant_entry_points for c in expected_content])

        # [print(n.function_info) for n in self.call_graph.get_descendant_entry_points(call)]

        # Assert
        self.assertEqual(expected_count, len(descendant_entry_points))
        self.assertTrue(all_found)

    def test_descendant_exit_points(self):
        # Arrange
        call = Call("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_count = 5
        expected_content = [Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")]

        # Act
        descendant_exit_points = self.formatter.get_descendant_exit_points(call)
        all_found = all([c in descendant_exit_points for c in expected_content])

        # [print('Call("' + n.function_info + '"),') for n in self.call_graph.get_descendant_exit_points(call)]

        # Assert
        self.assertEqual(expected_count, len(descendant_exit_points))
        self.assertTrue(all_found)

    def test_descendants_entry_point_ratio(self):
        # Arrange
        call = Call("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_value = "0.07142857142857142"

        # Act
        ratio = self.formatter.get_descendants_entry_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_descendants_exit_point_ratio(self):
        # Arrange
        call = Call("main() <int main (void) at ./src/helloworld.c:58>:")
        expected_value = "0.35714285714285715"

        # Act
        ratio = self.formatter.get_descendants_exit_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_ancestor_entry_points(self):
        # Arrange
        call = Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")
        expected_count = 1
        expected_content = [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        ancestor_entry_points = self.formatter.get_ancestor_entry_points(call)
        all_found = all([c in ancestor_entry_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(ancestor_entry_points))
        self.assertTrue(all_found)

    def test_ancestor_exit_points(self):
        # Arrange
        call = Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")
        expected_count = 2
        expected_content = [Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("main() <int main (void) at ./src/helloworld.c:58>:")]

        # Act
        ancestor_exit_points = self.formatter.get_ancestor_exit_points(call)
        all_found = all([c in ancestor_exit_points for c in expected_content])

        # Assert
        self.assertEqual(expected_count, len(ancestor_exit_points))
        self.assertTrue(all_found)

    def test_ancestors_entry_point_ratio(self):
        # Arrange
        call = Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:")
        expected_value = "0.3333333333333333"

        # Act
        ratio = self.formatter.get_ancestors_entry_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

    def test_ancestors_exit_point_ratio(self):
        # Arrange
        call = Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")
        expected_value = "0.5"

        # Act
        ratio = self.formatter.get_ancestors_exit_point_ratio(call)

        # Assert
        self.assertEqual(expected_value, ratio)

if __name__ == '__main__':
    unittest.main()