__author__ = 'kevin'

import unittest
import os

from loaders.cflow_loader import CflowLoader


class CflowLoaderTestCase(unittest.TestCase):

    def test_load_call_graph(self):
        # Arrange
        test_loader = CflowLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               "helloworld/cflow.callgraph.txt"),
                                  False)
        expected_content = ['GreeterSayHiTo helloworld.c',
                            'greet_a helloworld.c',
                            'printf',
                            'greet greetings.c',
                            'functionPtr helloworld.c',
                            'recursive_b greetings.c',
                            'new_Greeter helloworld.c',
                            'recursive_a greetings.c',
                            'addInt helloworld.c',
                            'greet_b helloworld.c',
                            'scanf',
                            'main helloworld.c',
                            'malloc',
                            'GreeterSayHi helloworld.c',
                            'puts']

        # Act
        test_graph = test_loader.load_call_graph()
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = all([n in nodes for n in expected_content]) and all([n in expected_content for n in nodes])

        # Assert
        self.assertEqual(15, len(nodes))
        self.assertTrue(all_nodes_found)


if __name__ == '__main__':
    unittest.main()
