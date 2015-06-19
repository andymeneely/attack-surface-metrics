import unittest
import os

from attacksurfacemeter.call import Call
from attacksurfacemeter.loaders.multigprof_loader import MultigprofLoader


class MultigprofLoaderTestCase(unittest.TestCase):
    def test_load_call_graph(self):
        # Arrange
        sources = [
            "multigprof/multigprof.one.callgraph.txt", 
            "multigprof/multigprof.two.callgraph.txt"
        ]
        sources = [os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 
            source
        ) for source in sources]
        test_loader = MultigprofLoader(sources, False)

        # Act
        test_graph = test_loader.load_call_graph()

        # Loader Errors

        # Assert
        self.assertEqual(0, len(test_loader.error_messages))

        # Nodes and node attributes
        expected_content = ["main multigprof.c",
            "fibonacci multigprof.c",
            "factorial multigprof.c"
        ]
        nodes = [n.identity for n in test_graph.nodes()]
        all_nodes_found = (all([n in nodes for n in expected_content]) and 
            all([n in expected_content for n in nodes]))

        # Assert
        self.assertEqual(3, len(nodes))
        self.assertTrue(all_nodes_found)
        for (node,attrs) in test_graph.nodes(data=True):
            self.assertTrue('tested' in attrs and attrs['tested'])

        # Edges and edge attributes
        expected_content = [
            (
                Call.from_gprof(
                    "                0.00    0.00       1/10      "
                    "    main (multigprof.c:35 @ 804861e) [25]"
                ),
                Call.from_gprof(
                    "                0.00    0.00       9/10      "
                    "    factorial (multigprof.c:7 @ 8048563) [7]"
                )
            ),
            (
                Call.from_gprof(
                    "                0.00    0.00       9/10      "
                    "    factorial (multigprof.c:7 @ 8048563) [7]"
                ),
                Call.from_gprof(
                    "[1]      0.0    0.00    0.00      10         "
                    "factorial (multigprof.c:4 @ 804854d) [1]"
                ),
            ),
            (
                Call.from_gprof(
                    "                0.00    0.00       1/1       "
                    "    main (multigprof.c:41 @ 8048674) [28]"
                ),
                Call.from_gprof(
                    "[1]      0.0    0.00    0.00       1         "
                    "fibonacci (multigprof.c:11 @ 8048577) [1]"
                )
            ),
        ]

        # Act
        edges = test_graph.edges()
        all_calls_found = all([c in edges for c in expected_content])

        # Assert
        self.assertEqual(3, len(edges))
        self.assertTrue(all_calls_found)
        for (u,v,attrs) in test_graph.edges(data=True):
            self.assertTrue('gprof' in attrs and attrs['gprof'] == 'gprof')

if __name__ == '__main__':
    unittest.main()
