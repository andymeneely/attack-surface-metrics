__author__ = 'kevin'

import unittest
from loaders.gprof_loader import GprofLoader


class CflowLoaderTestCase(unittest.TestCase):

    def test_load_call_graph(self):
        # Arrange
        test_loader = GprofLoader("/home/kevin/Documents/attack-surface-metrics/tests/helloworld/gprof.callgraph.txt",
                                  False)
        expected_content = ['GreeterSayHiTo helloworld.c',
                            'greet_a helloworld.c',
                            'recursive_a greetings.c',
                            'addInt helloworld.c',
                            'greet_b helloworld.c',
                            'recursive_b greetings.c',
                            'main helloworld.c',
                            'new_Greeter helloworld.c',
                            'greet greetings.c',
                            'GreeterSayHi helloworld.c']

        # Act
        test_graph = test_loader.load_call_graph()
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = all([n in nodes for n in expected_content]) and all([n in expected_content for n in nodes])

        # Assert
        self.assertEqual(10, len(nodes))
        self.assertTrue(all_nodes_found)


if __name__ == '__main__':
    unittest.main()
