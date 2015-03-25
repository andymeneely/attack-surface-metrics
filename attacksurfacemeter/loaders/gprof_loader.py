__author__ = 'kevin'

import networkx as nx

from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.call import Call


class GprofLoader(BaseLoader):
    """"""

    header = "index % time    self  children    called     name\n"
    separator = "-----------------------------------------------\n"
    eof = "\x0c\n"

    def __init__(self, source, reverse):
        """Constructor for GprofLoader"""
        self.source = source

        self._error_messages = list()

    @property
    def error_messages(self):
        return self._error_messages

    def is_entry_line(self, line):
        return line.startswith("[")
        # return re.search(r"^\[\d+.*", line)

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

        # line_count = 0

        with open(self.source) as raw_call_graph:
            while True:
                line = raw_call_graph.readline()
                # line_count += 1
                # print(line_count)
                # print(line)

                if not header_passed:
                    if line == GprofLoader.header:
                        header_passed = True
                    continue

                else:  # if header_passed:
                    if self.is_entry_line(line):
                        try:
                            entry = Call.from_gprof(line)
                        except ValueError as e:
                            raise e

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
                        try:
                            if is_caller:
                                callers.append(Call.from_gprof(line))
                            else:
                                callees.append(Call.from_gprof(line))
                        except ValueError as e:
                            self._error_messages.append("Error: " + str(e) + " Input line: " + line)

        return call_graph