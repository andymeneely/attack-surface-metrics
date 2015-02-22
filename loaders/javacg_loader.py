__author__ = 'kevin'

import networkx as nx

from loaders.base_loader import BaseLoader
from attacksurfacemeter.call import Call


class JavaCGLoader(BaseLoader):
    """"""
    def __init__(self, source, reverse=False):
        """Constructor for JavaCGLoader"""
        self.source = source

    def load_call_graph(self):
        """
            Description.

            Comments.

            Returns:
                A call graph.
        """
        call_graph = nx.DiGraph()

        with open(self.source) as raw_call_graph:
            # line is like this:
            # M:com.example.kevin.helloandroid.Greeter:sayHelloInSpanish (M)java.lang.StringBuilder:toString
            for line in raw_call_graph:
                if line.startswith("M:"):
                    caller, callee = line.split(" ")
                    call_graph.add_edge(Call.from_javacg(caller), Call.from_javacg(callee))

        return call_graph