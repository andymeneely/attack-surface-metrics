__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader

class CallGraphCleaningOptionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_standard_library_calls(self):
        # Arrange
        call_graph = CallGraph.from_loader(
            CflowLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/cflow.callgraph.r.txt"), True))

        expected_content = [Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"),
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"),
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"),
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")]

        # Act
        call_graph.remove_standard_library_calls()
        nodes = call_graph.nodes
        all_calls_found = all([c in nodes for c in expected_content])

        # Assert
        self.assertEqual(11, len(nodes))
        self.assertTrue(all_calls_found)

    def test_remove_function_name_only_calls(self):
        # Arrange
        call_graph = CallGraph.from_loader(
            CflowLoader(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "helloworld/cflow.callgraph.r.mod.txt"), True))

        expected_content = [Call.from_cflow("greet() <void greet (int greeting_code) at ./src/greetings.c:14>:"),
                            Call.from_cflow("new_Greeter() <Greeter new_Greeter () at ./src/helloworld.c:38>:"),
                            Call.from_cflow("addInt() <int addInt (int n, int m) at ./src/helloworld.c:18>"),
                            Call.from_cflow("functionPtr() <int (*functionPtr) (int, int) at ./src/helloworld.c:23>"),
                            Call.from_cflow("GreeterSayHiTo() <void GreeterSayHiTo (int value) at ./src/helloworld.c:53>:"),
                            Call.from_cflow("recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):"),
                            Call.from_cflow("recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):"),
                            Call.from_cflow("main() <int main (void) at ./src/helloworld.c:58>:"),
                            Call.from_cflow("greet_b() <void greet_b (int i) at ./src/helloworld.c:82>:"),
                            Call.from_cflow("greet_a() <void greet_a (int i) at ./src/helloworld.c:76>:")]

        # Act
        call_graph.remove_function_name_only_calls()
        nodes = call_graph.nodes
        all_calls_found = all([c in call_graph.nodes for c in expected_content])

        # Assert
        self.assertEqual(10, len(nodes))
        self.assertTrue(all_calls_found)

if __name__ == '__main__':
    unittest.main()