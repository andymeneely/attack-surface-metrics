__author__ = 'kevin'

import subprocess
import os
import networkx as nx

from attacksurfacemeter.loaders.stack import Stack
from attacksurfacemeter.loaders.base_loader import BaseLoader
from attacksurfacemeter.call import Call


class CflowLoader(BaseLoader):
    """"""
    def __init__(self, source, reverse=False):
        """Constructor for CflowParser"""
        self.source = source
        self.is_reverse = reverse

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
        is_first_line = True
        parent = Stack()

        if os.path.isfile(self.source):
            raw_call_graph = open(self.source)
            readline = lambda: raw_call_graph.readline()

        elif os.path.isdir(self.source):
            raw_call_graph = self._exec_cflow(self.is_reverse)
            readline = lambda: raw_call_graph.stdout.readline().decode(encoding='UTF-8')

        while True:
            line = readline()

            if line == '':
                break

            current = Call.from_cflow(line)

            if not is_first_line:
                if current.level > previous.level:
                    parent.push(previous)
                elif current.level < previous.level:
                    for t in range(previous.level - current.level):
                        parent.pop()

                if parent.top:
                    call_graph.add_node(current, {'tested': False})
                    call_graph.add_node(parent.top, {'tested': False})

                    if not self.is_reverse:
                        call_graph.add_edge(parent.top, current, 
                            {'cflow': 'cflow'})
                    else:
                        call_graph.add_edge(current, parent.top, 
                            {'cflow': 'cflow'})

            previous = current
            is_first_line = False

        return call_graph

    def _exec_cflow(self, is_reverse):
        """
            Creates a subprocess.Popen instance representing the cflow call.

            Args:
                is_reverse: Boolean specifying whether the graph generation software (cflow) should use the reverse
                    algorithm.

            Returns:
                A subprocess.Popen instance representing the cflow call.
        """
        if is_reverse:
            cflow_exe = 'run_cflow_r.sh'
        else:
            cflow_exe = 'run_cflow.sh'

        dirname = os.path.dirname(os.path.realpath(__file__))
        proc = subprocess.Popen(['sh', os.path.join(dirname, cflow_exe), self.source],
                                stdout=subprocess.PIPE)

        return proc