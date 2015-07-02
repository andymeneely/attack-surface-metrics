import multiprocessing
import os
import unittest

from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class GprofLoaderCatchallTestCase(unittest.TestCase):
    def test_load_call_graph_empty_file(self):
        # Act
        target = GprofLoader(
            os.path.join(os.path.dirname(
                os.path.realpath(__file__)),
                'helloworld/empty.gprof.callgraph.txt'
            ),
            False
        )

        # Using a separate process to ensure the loading of an emtpy call graph
        # completes within a reasonable time (see timeout below).
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            name='p.gprof',
            target=self._wrapper,
            args=(target.load_call_graph, queue)
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

    def _wrapper(self, target, queue, args=(), kwargs={}):
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
