__author__ = 'kevin'

import re
import networkx as nx

from attacksurfacemeter import GprofCall


class GprofLoader():
    """"""

    header = "index % time    self  children    called     name\n"
    separator = "-----------------------------------------------\n"
    eof = "\x0c\n"

    def __init__(self, source, reverse):
        """Constructor for GprofLoader"""
        self.source = source

        # re.search(r"(\[.+\]) ( +) ((\d+\.\d+) ( +)){3} (\d+) ( +) (\w+) (\(.+\)) (\[.+\])", line).group(0)
        # line = text.split("-----------------------------------------------")[10].split("\n")[-1]
        # list = [l for l in open("tests/helloworld/gprof-call-graph.txt")]
        # text = "".join(list)

        # >>> import re
        # >>> for l in text.split("-----------------------------------------------")[10].split("\n"):
        # ...     if re.search(r"(\[.+\]) ( +) ((\d+\.\d+) ( +)){3} (\d+) ( +) (\w+) (\(.+\)) (\[.+\])", l):
        # ...         l

        # >>> text.split("-----------------------------------------------")[10].split("\n").index(line)

        # re.search(r"(\[.+\]) ( +) ((\d+\.\d+) ( +)){3} (\d+) ( +) (\w+) (\[.+\])", line).group(0)

        pass

    def is_entry_line(self, line):
        return re.search(r"^\[.+\].*", line)

    def load_call_graph(self):
        """
            Generates the Call Graph as a networkx.DiGraph object.

            Invokes the call grap generation software (cflow) and creates a networkx.DiGraph instance that represents
            the analyzed source code's Call Graph.

            Args:
                is_reverse: Boolean specifying whether the graph generation software (cflow) should use the reverse
                    algorithm.

            Returns:
                None
        """
        call_graph = nx.DiGraph()

        header_passed = False

        entry = None

        is_caller = True
        callers = list()
        callees = list()

        with open(self.source) as raw_call_graph:
            while True:
                line = raw_call_graph.readline()

                if not header_passed:
                    if line == GprofLoader.header:
                        header_passed = True
                    continue

                else:  # if header_passed:
                    if self.is_entry_line(line):
                        entry = GprofCall(line)
                        call_graph.add_node(entry)
                        is_caller = False

                    elif line == GprofLoader.separator:
                        for caller in callers:
                            call_graph.add_edge(caller, entry)
                        callers.clear()

                        for callee in callees:
                            call_graph.add_edge(entry, callee)
                        callees.clear()

                        is_caller = True

                    elif line == GprofLoader.eof:
                        break

                    else:
                        if is_caller:
                            callers.append(GprofCall(line))
                        else:
                            callees.append(GprofCall(line))

        return call_graph