__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.loaders.cflow_loader import CflowLoader


class CflowLoaderTestCase(unittest.TestCase):

    def test_load_call_graph(self):
        # Arrange
        test_loader = CflowLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "helloworld/cflow.callgraph.txt"),
                                  False)
        expected_content = ['GreeterSayHiTo ./src/helloworld.c',
                            'greet_a ./src/helloworld.c',
                            'printf',
                            'greet ./src/greetings.c',
                            'functionPtr ./src/helloworld.c',
                            'recursive_b ./src/greetings.c',
                            'new_Greeter ./src/helloworld.c',
                            'recursive_a ./src/greetings.c',
                            'addInt ./src/helloworld.c',
                            'greet_b ./src/helloworld.c',
                            'scanf',
                            'main ./src/helloworld.c',
                            'malloc',
                            'GreeterSayHi ./src/helloworld.c',
                            'puts']

        # Act
        test_graph = test_loader.load_call_graph()
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = all([n in nodes for n in expected_content]) and all([n in expected_content for n in nodes])

        # Assert
        self.assertEqual(15, len(nodes))
        self.assertTrue(all_nodes_found)

    def test_load_call_graph_edge_attributes(self):
        # Arrange
        test_loader = CflowLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "helloworld/cflow.callgraph.txt"
            ),
            False
        )

        # Act
        test_graph = test_loader.load_call_graph()

        # Assert
        for (u, v, d) in test_graph.edges(data=True):
            self.assertFalse('cflow' not in d)

if __name__ == '__main__':
    unittest.main()
