__author__ = 'kevin'

import unittest
from attacksurfacemeter.stack import Stack
from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph


class StackTestCase(unittest.TestCase):

    def test_push(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        # Assert
        self.assertEqual(len(test_stack), 2)

    def test_pop(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        popped_value = test_stack.pop()

        # Assert
        self.assertEqual(popped_value, 2)
        self.assertEqual(len(test_stack), 1)

    def test_top(self):
        # Arrange
        test_stack = Stack()

        # Act
        test_stack.push(1)
        test_stack.push(2)

        # Assert
        self.assertEqual(test_stack.top, 2)


class CallTestCase(unittest.TestCase):

    def test_identity_function_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.identity, "printf()")

    def test_identity_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.identity, "xstrdup()<char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89>")

    def test_function_name_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_name, "printf()")

    def test_function_name_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_name, "xstrdup()")

    def test_function_signature_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertIsNone(test_call.function_signature)

    def test_function_signature_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertEqual(test_call.function_signature, "<char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89>")

    def test_is_input_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = Call(cflow_line)

        # Assert
        self.assertTrue(test_call.is_input_function())

    def test_is_not_input_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_not_input_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_output_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = Call(cflow_line)

        # Assert
        self.assertTrue(test_call.is_output_function())

    def test_is_not_output_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_is_not_output_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = Call(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_equal(self):
        # Arrange
        cflow_line = "getchar()"
        test_call_1 = Call(cflow_line)
        test_call_2 = Call(cflow_line)

        # Assert
        self.assertEqual(test_call_1, test_call_2)

    def test_not_equal(self):
        # Arrange
        cflow_line_1 = "getchar()"
        cflow_line_2 = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call_1 = Call(cflow_line_1)
        test_call_2 = Call(cflow_line_2)

        # Assert
        self.assertNotEqual(test_call_1, test_call_2)


class CallGraphTestCase(unittest.TestCase):

    def setUp(self):
        self.call_graph = CallGraph("./helloworld")

    def test_entry_points_count(self):
        # Act
        entry_points_count = len(self.call_graph.entry_points)

        # Assert
        self.assertEqual(entry_points_count, 1)

    def test_exit_points_count(self):
        # Act
        exit_points_count = len(self.call_graph.exit_points)

        # Assert
        self.assertEqual(exit_points_count, 6)

    def test_entry_points_content(self):
        # Arrange
        expected_content = [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")]

        # Act
        entry_points = self.call_graph.entry_points
        all_entry_points_encountered = all([c in entry_points for c in expected_content])

        # Assert
        self.assertTrue(all_entry_points_encountered)

    def test_exit_points_content(self):
        # Arrange
        expected_content = [Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")]

        # Act
        exit_points = self.call_graph.exit_points
        all_exit_points_encountered = all([c in exit_points for c in expected_content])

        # for c in exit_points:
        #     print('Call("' + c.function_info + '"),')

        # Assert
        self.assertTrue(all_exit_points_encountered)

    def test_shortest_path(self):
        # Arrange
        n1 = Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:")
        n2 = Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")

        expected_content = [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")]

        # Act
        call_path = self.call_graph.shortest_path(n1, n2)
        all_calls_found = all([c in call_path for c in expected_content])

        # for c in call_path:
        #     print('Call("' + c.function_info + '"),')

        # Assert
        self.assertEqual(len(call_path), 3)
        self.assertTrue(all_calls_found)

    def test_nodes(self):
        # Arrange
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
        nodes = self.call_graph.nodes
        all_calls_found = all([c in nodes for c in expected_content])

        # for c in nodes:
        #     print('Call("' + c.function_info + '"),')

        # Assert
        self.assertEqual(len(nodes), 15)
        self.assertTrue(all_calls_found)

    def test_edges(self):
        # Arrange
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
        edges = self.call_graph.edges
        all_calls_found = all([c in edges for c in expected_content])

        # for e in edges:
        #     print('(Call("' + e[0].function_info + '"), Call("' + e[1].function_info + '")),')

        # Assert
        self.assertEqual(len(edges), 22)
        self.assertTrue(all_calls_found)

    def test_execution_paths(self):
        # Arrange
        expected_content = [[Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                             Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")],
                            [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R): [see 7]")],
                            [Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>: [see 3]")]]

        # Act
        paths = self.call_graph.execution_paths
        all_paths_found = all([p in paths for p in expected_content])

        # for p in paths:
        #     print("[")
        #     for c in p:
        #         print('Call("' + c.function_info + '"),')
        #     print("],")

        # Assert
        self.assertEqual(len(paths), 3)
        self.assertTrue(all_paths_found)

    def test_avg_execution_path(self):
        # Act
        average = self.call_graph.avg_execution_path_length

        # Assert
        self.assertEqual(average, 2.3333333333333335)

    def test_median_execution_path(self):
        # Act
        median = self.call_graph.median_execution_path_length

        # Assert
        self.assertEqual(median, 2)

    def test_entry_clustering_coefficient(self):
        # Act
        coefficient = self.call_graph.entry_points_clustering

        # Assert
        self.assertEqual(coefficient, 0.0)

    def test_exit_clustering_coefficient(self):
        # Act
        coefficient = self.call_graph.exit_points_clustering

        # Assert
        self.assertEqual(coefficient, 0.1111111111111111)

    def test_execution_paths_for_call(self):
        # Arrange
        call = Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")

        expected_content = [[Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                             Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                             Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")]]

        # Act
        paths = self.call_graph.get_execution_paths_for(call)
        all_paths_found = all([p in paths for p in expected_content])
        call_in_all_paths = all([call in p for p in paths])

        # Assert
        self.assertEqual(len(paths), 1)
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
        self.assertEqual(first_distance[0]['distance'], 0)
        self.assertEqual(second_distance[0]['distance'], 1)
        self.assertEqual(third_distance[0]['distance'], 2)

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
        self.assertEqual(first_distance[0]['distance'], 2)
        self.assertEqual(second_distance[0]['distance'], 1)
        self.assertEqual(third_distance[0]['distance'], 0)

    def test_all_betweenness(self):
        # Arrange
        expected_content = {Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.016483516483516484,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.01098901098901099,
                            Call("gets()"): 0.0,
                            Call("puts()"): 0.0,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 0.008241758241758242,
                            Call("printf()"): 0.0,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.0027472527472527475,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0.0,
                            Call("malloc()"): 0.0,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.01098901098901099,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 0.013736263736263738,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.0027472527472527475,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.01098901098901099}

        # Act
        betweennesses = self.call_graph.get_betweenness()
        all_values_correct = all([betweennesses[c] == expected_content[c] for c in betweennesses])

        # for c in betweennesses:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_betweenness()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(betweennesses), 15)

    def test_node_specific_betweenness(self):
        # Arrange
        expected_value = 0.016483516483516484
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        betweenness = self.call_graph.get_betweenness(call)

        # Assert
        self.assertEqual(betweenness, expected_value)

    def test_all_closeness(self):
        # Arrange
        expected_content = {Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.22857142857142856,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call("gets()"): 0.0,
                            Call("puts()"): 0.0,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 0.22321428571428573,
                            Call("printf()"): 0.0,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0.6666666666666666,
                            Call("malloc()"): 0.0,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.07142857142857142,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 0.2857142857142857,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285}

        # Act
        closenesses = self.call_graph.get_closeness()
        all_values_correct = all([closenesses[c] == expected_content[c] for c in closenesses])

        # for c in closenesses:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_closeness()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(closenesses), 15)

    def test_node_specific_closeness(self):
        # Arrange
        expected_value = 0.22857142857142856
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        closeness = self.call_graph.get_closeness(call)

        # Assert
        self.assertEqual(closeness, expected_value)

    def test_all_degree_centrality(self):
        # Arrange
        expected_content = {Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 0.21428571428571427,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.2857142857142857,
                            Call("puts()"): 0.14285714285714285,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.2857142857142857,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.21428571428571427,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.14285714285714285,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0.5,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.07142857142857142,
                            Call("printf()"): 0.3571428571428571,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 0.2857142857142857,
                            Call("gets()"): 0.07142857142857142,
                            Call("malloc()"): 0.07142857142857142,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.2857142857142857,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.14285714285714285,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.07142857142857142}

        # Act
        degrees = self.call_graph.get_degree_centrality()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_all_in_degree_centrality(self):
        # Arrange
        expected_content = {Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.14285714285714285,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 0.07142857142857142,
                            Call("puts()"): 0.14285714285714285,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 0.07142857142857142,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.07142857142857142,
                            Call("gets()"): 0.07142857142857142,
                            Call("printf()"): 0.3571428571428571,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.07142857142857142,
                            Call("malloc()"): 0.07142857142857142,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.07142857142857142,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0.0}

        # Act
        degrees = self.call_graph.get_in_degree_centrality()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_all_out_degree_centrality(self):
        # Arrange
        expected_content = {Call("malloc()"): 0.0,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 0.21428571428571427,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 0.14285714285714285,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 0.07142857142857142,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 0.21428571428571427,
                            Call("puts()"): 0.0,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0.0,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0.0,
                            Call("gets()"): 0.0,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 0.14285714285714285,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 0.07142857142857142,
                            Call("printf()"): 0.0,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0.5,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 0.14285714285714285,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 0.07142857142857142}

        # Act
        degrees = self.call_graph.get_out_degree_centrality()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_node_specific_degree_centrality(self):
        # Arrange
        expected_value = 0.2857142857142857
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_degree_centrality(call)

        # Assert
        self.assertEqual(degree, expected_value)

    def test_node_specific_in_degree_centrality(self):
        # Arrange
        expected_value = 0.07142857142857142
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_in_degree_centrality(call)

        # Assert
        self.assertEqual(degree, expected_value)

    def test_node_specific_out_degree_centrality(self):
        # Arrange
        expected_value = 0.21428571428571427
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_out_degree_centrality(call)

        # Assert
        self.assertEqual(degree, expected_value)
    
    def test_all_degree(self):
        # Arrange
        expected_content = {Call("malloc()"): 1,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 4,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 3,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 2,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 4,
                            Call("puts()"): 2,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 1,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 1,
                            Call("gets()"): 1,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 4,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 2,
                            Call("printf()"): 5,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 7,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 4,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 3}

        # Act
        degrees = self.call_graph.get_degree()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_all_in_degree(self):
        # Arrange
        expected_content = {Call("malloc()"): 1,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 1,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 1,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 1,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 1,
                            Call("puts()"): 2,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 1,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 1,
                            Call("gets()"): 1,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 2,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 1,
                            Call("printf()"): 5,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 0,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 2,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 2}

        # Act
        degrees = self.call_graph.get_in_degree()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_all_out_degree(self):
        # Arrange
        expected_content = {Call("malloc()"): 0,
                            Call("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"): 3,
                            Call("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:"): 2,
                            Call("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"): 1,
                            Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"): 3,
                            Call("puts()"): 0,
                            Call("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"): 0,
                            Call("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"): 0,
                            Call("gets()"): 0,
                            Call("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"): 2,
                            Call("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"): 1,
                            Call("printf()"): 0,
                            Call("main() <int main (void) at ./src/helloworld.c:58>:"): 7,
                            Call("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"): 2,
                            Call("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"): 1}

        # Act
        degrees = self.call_graph.get_out_degree()
        all_values_correct = all([degrees[c] == expected_content[c] for c in degrees])

        # for c in degrees:
        #     print('Call("' + c.function_info + '"): ' + str(g.get_degree_centrality()[c]) + ',')

        # Assert
        self.assertTrue(all_values_correct)
        self.assertEqual(len(degrees), 15)

    def test_node_specific_degree(self):
        # Arrange
        expected_value = 4
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_degree(call)

        # Assert
        self.assertEqual(degree, expected_value)

    def test_node_specific_in_degree(self):
        # Arrange
        expected_value = 1
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_in_degree(call)

        # Assert
        self.assertEqual(degree, expected_value)

    def test_node_specific_out_degree(self):
        # Arrange
        expected_value = 3
        call = Call("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:")

        # Act
        degree = self.call_graph.get_out_degree(call)

        # Assert
        self.assertEqual(degree, expected_value)


class CallGraphReverseTestCase(CallGraphTestCase):
    def setUp(self):
        self.call_graph = CallGraph("./helloworld", True)


if __name__ == '__main__':
    unittest.main()