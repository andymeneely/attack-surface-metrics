__author__ = 'kevin'

import unittest
import os

from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class GprofLoaderTestCase(unittest.TestCase):
    def test_load_call_graph(self):
        # Arrange
        test_loader = GprofLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "helloworld/gprof.callgraph.txt"),
                                  False)
        expected_content = ['GreeterSayHiTo ./src/helloworld.c',
                            'greet_a ./src/helloworld.c',
                            'recursive_a ./src/greetings.c',
                            'addInt ./src/helloworld.c',
                            'greet_b ./src/helloworld.c',
                            'recursive_b ./src/greetings.c',
                            'main ./src/helloworld.c',
                            'new_Greeter ./src/helloworld.c',
                            'greet ./src/greetings.c',
                            'GreeterSayHi ./src/helloworld.c']

        # Act
        test_graph = test_loader.load_call_graph()
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = all([n in nodes for n in expected_content]) and all([n in expected_content for n in nodes])

        # Assert
        self.assertEqual(10, len(nodes))
        self.assertTrue(all_nodes_found)

    def test_load_call_graph_edge_attributes(self):
        # Arrange
        test_loader = GprofLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "helloworld/gprof.callgraph.txt"
            ),
            False
        )

        # Act
        test_graph = test_loader.load_call_graph()
        edges = [edge for edge in test_graph.edges() 
            if 'gprof' in test_graph.get_edge_data(*edge)]

        # Assert
        self.assertEqual(len(test_graph.edges()), len(edges))

if __name__ == '__main__':
    unittest.main()
