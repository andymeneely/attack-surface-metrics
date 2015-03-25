__author__ = 'kevin'

import networkx as nx

from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.call import Call


class JavaCGLoader(BaseLoader):
    """"""
    def __init__(self, source, app_packages=[]):
        """Constructor for JavaCGLoader"""
        self.source = source
        self.app_packages = app_packages

    def load_call_graph(self):
        """
            Description.

            Comments.

            Returns:
                A call graph.
        """
        call_graph = nx.DiGraph()

        if self.app_packages:
            condition_to_add = lambda line: line.startswith("M:") and self._contains_call_in_package(line)
        else:
            condition_to_add = lambda line: line.startswith("M:")

        with open(self.source) as raw_call_graph:
            # line is like this:
            # M:com.example.kevin.helloandroid.Greeter:sayHelloInSpanish (M)java.lang.StringBuilder:toString.
            for line in raw_call_graph:
                if condition_to_add(line):
                    caller, callee = line.split(" ")
                    call_graph.add_edge(Call.from_javacg(caller), Call.from_javacg(callee))

        return call_graph

    def _contains_call_in_package(self, line):
            return any([(p in line) for p in self.app_packages])
