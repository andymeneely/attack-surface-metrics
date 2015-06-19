__author__ = 'kevin'

import os
import multiprocessing
import sys

import networkx as nx

from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class MultigprofLoader(BaseLoader):
    """"""

    def __init__(self, sources, reverse=False, processes=1):
        """Constructor for MultigprofLoader"""
        self.source = 'multiple'
        self.reverse = reverse
        self.sources = sources
        self._error_messages = list()
        self._processes = processes

    @property
    def error_messages(self):
        return self._error_messages

    def load_call_graph(self):
        """
            Generates a Call Graph as a networkx.DiGraph object. The call 
            graph generated is an aggregate of multiple call graphs output by
            GNU gprof.
        """
        call_graph = None

        manager = multiprocessing.Manager()
        sync_queue = manager.Queue(maxsize=50)
        out_queue = manager.Queue(maxsize=1)

        process = multiprocessing.Process(
            name='process.merger',
            target=self._merge_call_graph,
            args=(sync_queue, out_queue)
        )
        process.start()

        with multiprocessing.Pool(self._processes) as pool:
            pool.starmap(
                func=self._load_call_graph,
                iterable=[
                    (index, sync_queue) for index in range(len(self.sources))
                ]
            )

        process.join()

        (call_graph, self._error_messages) = out_queue.get(block=True)

        return call_graph

    def _load_call_graph(self, index, sync_queue):
        loader = GprofLoader(self.sources[index], reverse=self.reverse)
        call_graph = loader.load_call_graph()

        sync_queue.put((call_graph, loader.error_messages), block=True)

    def _merge_call_graph(self, sync_queue, out_queue):
        call_graph = nx.DiGraph()
        error_messages = list()

        remaining = len(self.sources)

        while remaining > 0:
            (_call_graph, _error_messages) = sync_queue.get(block=True)
            call_graph.add_nodes_from(_call_graph.nodes(data=True))
            call_graph.add_edges_from(_call_graph.edges(data=True))
            error_messages.extend(_error_messages)

            remaining -= 1

            if 'DEBUG' in os.environ:
                self._print_status(remaining)
        
        out_queue.put((call_graph, error_messages), block=True)

    def _print_status(self, remaining):
        sys.stdout.write('\r')
        sys.stdout.write('{0:5d} remaining'.format(remaining))
        sys.stdout.flush()

