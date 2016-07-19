import os
import multiprocessing
import sys

import networkx as nx

from attacksurfacemeter.granularity import Granularity
from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class MultigprofLoader(BaseLoader):
    """"""

    def __init__(self, sources, reverse=False, defenses=None,
                 vulnerabilities=None, processes=1):
        """Constructor for MultigprofLoader.

        Parameters
        ----------
        source : str
            The absolute path to a text file containing the call graph
            generated using gprof.
        reverse : bool, optional
            Parameter irrelevant.
        defenses : list, optional
            A list of Call objects, each representing a designed defense in the
            system.
        vulnerabilities : list, optional
            A list of Call objects, each representing a vulnerable function in
            the system.
        processes : int, optional
            Number of processes to spawn when aggregating multiple gprof call
            graphs.
        """
        super(MultigprofLoader, self).__init__(
            'multiple', reverse, defenses, vulnerabilities
        )
        self.sources = sources
        self._processes = processes

    def load_call_graph(self, granularity=Granularity.FUNC):
        """Load an aggregate of multiple call graphs generated by gprof.

        Parameters
        ----------
        granularity : str
            The granularity at which the call graph must be loaded. See
            attacksurfacemeter.granularity.Granularity for available choices.

        Returns
        -------
        call_graph : networkx.DiGraph
            An object representing the call graph.
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
                    (index, granularity, sync_queue)
                    for index in range(len(self.sources))
                ],
                chunksize=1
            )

        process.join()

        (call_graph, self._errors) = out_queue.get(block=True)

        return call_graph

    def _load_call_graph(self, index, granularity, sync_queue):
        loader = GprofLoader(
            self.sources[index], self.is_reverse, self.defenses,
            self.vulnerabilities
        )
        call_graph = loader.load_call_graph(granularity)

        sync_queue.put((call_graph, loader.errors), block=True)

    def _merge_call_graph(self, sync_queue, out_queue):
        call_graph = nx.DiGraph()
        attributes = dict()
        errors = list()

        count = len(self.sources)
        index = 0
        while index < count:
            (_call_graph, _errors) = sync_queue.get(block=True)
            index += 1
            if 'DEBUG' in os.environ:
                self._print_status(index, count)
            for (node, attrs) in _call_graph.nodes(data=True):
                if 'frequency' in attrs and node in attributes:
                    attrs['frequency'] = attributes[node] + 1
                call_graph.add_node(node, **attrs)
            call_graph.add_edges_from(_call_graph.edges(data=True))
            attributes = nx.get_node_attributes(call_graph, 'frequency')

            errors.extend(_errors)

        out_queue.put((call_graph, errors), block=True)

    def _print_status(self, index, count):
        sys.stdout.write('\r')
        sys.stdout.write('\033[K')
        sys.stdout.write('Processing {0:4d}/{1:4d}'.format(index, count))
        sys.stdout.flush()
