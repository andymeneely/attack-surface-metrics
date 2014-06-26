__author__ = 'kevin'

import subprocess
import os
import statistics as stat
import networkx as nx
import matplotlib.pyplot as plt

from attacksurfacemeter.stack import Stack
from attacksurfacemeter.call import Call


class CallGraph():

    def __init__(self, source_dir, reverse=False):
        self.source_dir = source_dir
        self.call_graph = nx.DiGraph()

        self._entry_points = set()
        self._exit_points = set()

        self._generate(reverse)

    def _generate(self, is_reverse):
        is_first_line = True
        parent = Stack()

        proc = self._exec_cflow(is_reverse)

        while True:
            line = proc.stdout.readline().decode(encoding='UTF-8')

            if line == '':
                break

            current = Call(line)

            if not is_first_line:
                if current.level > previous.level:
                    parent.push(previous)
                elif current.level < previous.level:
                    for t in range(previous.level - current.level):
                        parent.pop()

                if parent.top:
                    if not is_reverse:
                        self.call_graph.add_edge(parent.top, current)
                    else:
                        self.call_graph.add_edge(current, parent.top)

            previous = current
            is_first_line = False

    def _exec_cflow(self, is_reverse):
        dirname = os.path.dirname(os.path.realpath(__file__))

        if is_reverse:
            cflow_exe = 'run_cflow_r.sh'
        else:
            cflow_exe = 'run_cflow.sh'

        proc = subprocess.Popen(['sh', os.path.join(dirname, cflow_exe), self.source_dir],
                                stdout=subprocess.PIPE)

        return proc


    def _select_nodes(self, predicate):
        return [n for n in self.call_graph.nodes() if predicate(n)]

    @property
    def entry_points(self):
        if not self._entry_points:
            self._entry_points = self._select_nodes(lambda n: any([s.is_input_function() for s
                                                                   in self.call_graph.successors(n)]))
        return self._entry_points

    @property
    def exit_points(self):
        if not self._exit_points:
            self._exit_points = self._select_nodes(lambda n: any([s.is_output_function() for s
                                                                  in self.call_graph.successors(n)]))
        return self._exit_points

    @property
    def nodes(self):
        return self.call_graph.nodes()

    @property
    def edges(self):
        return self.call_graph.edges()

    def save_png(self):
        nx.draw(self.call_graph)
        plt.savefig(os.path.basename(os.path.normpath(self.source_dir)) + ".png")
        plt.clf()
    
    def shortest_path(self, source, target):
        return nx.shortest_path(self.call_graph, source, target)

    @property
    def execution_paths(self):
        paths = []

        for entry_point in self.entry_points:
            for exit_point in self.exit_points:
                if nx.has_path(self.call_graph, entry_point, exit_point):
                    paths.append(nx.shortest_path(self.call_graph, entry_point, exit_point))

        return paths

    @property
    def avg_execution_path_length(self):
        return stat.mean([len(p) for p in self.execution_paths])

    @property
    def median_execution_path_length(self):
        return stat.median([len(p) for p in self.execution_paths])

    def average_clustering(self, nodes):
        return nx.average_clustering(self.call_graph.to_undirected(), nodes)

    @property
    def entry_points_clustering(self):
        return self.average_clustering(self.entry_points)

    @property
    def exit_points_clustering(self):
        return self.average_clustering(self.exit_points)
