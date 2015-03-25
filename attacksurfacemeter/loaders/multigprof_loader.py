__author__ = 'kevin'

import networkx as nx

from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.loaders.gprof_loader import GprofLoader


class MultigprofLoader(BaseLoader):
    """"""

    def __init__(self, sources, reverse=False):
        """Constructor for MultigprofLoader"""
        self.source = 'multiple'
        self.reverse = reverse
        
        self.sources = sources

        self._error_messages = list()

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
        for source in self.sources:
            _gprof_loader = GprofLoader(source, reverse=self.reverse)
            _gprof_call_graph = _gprof_loader.load_call_graph()

            if call_graph:
                call_graph.add_edges_from(
                    _gprof_call_graph.edges()
                )
            else:
                call_graph = _gprof_call_graph

            self.error_messages.append(_gprof_loader.error_messages)

        return call_graph
