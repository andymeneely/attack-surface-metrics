__author__ = 'kevin'

import multiprocessing
import os
import unittest

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
        
        # Assert
        for (u, v, d) in test_graph.edges(data=True):
            self.assertFalse('gprof' not in d)

    def test_load_empty_call_graph(self):
        # Arrange
        test_loader = GprofLoader(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "helloworld/empty.gprof.callgraph.txt"
            ),
            False
        )

        # Act

        # Using a separate process to ensure the loading of an emtpy call graph
        # completes within a reasonable time (see timeout below).
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            name='p.gprof',
            target=self.__wrapper__,
            args=(test_loader.load_call_graph, queue)
        )
        process.start()
        timeout = 1
        process.join(timeout=timeout)
        is_alive = process.is_alive()
        if is_alive:
            process.terminate()
        self.assertFalse(
            is_alive,
            msg=(
                'Process loading an empty gprof file has not terminated'
                ' even after {0} second(s).'.format(timeout)
            )
        )

        # Assert
        test_graph = queue.get()
        self.assertEqual(0, len(test_graph.nodes()))

    def __wrapper__(self, target, queue, args=(), kwargs={}):
        """Internal method to wrap the call to another function.

        Using a wrapper enables handling return parameters from a target
        function without having to modify the function itself.

        Parameters
        ----------
        target : function object
            The function to be wrapped.
        queue : Queue.Queue object
            Container for the return values from the wrapped function.
        args : tuple, optional
            Argument tuple for the wrapped function.
        kwargs : dictionary, optional
            Dictionary of keyword arguments for the wrapped function.
        """
        if args:
            if kwargs:
                queue.put(target(*args, **kwargs))
            else:
                queue.put(target(*args))
        else:
            queue.put(target())


if __name__ == '__main__':
    unittest.main()
