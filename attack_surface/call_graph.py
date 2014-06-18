__author__ = 'kevin'

import subprocess
import os

import networkx as nx
import matplotlib.pyplot as plt

from attack_surface.stack import Stack
from attack_surface.call import Call


class CallGraph():

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.call_graph = nx.DiGraph()

        self._entry_points = set()
        self._exit_points = set()

        self._generate()

    def _generate(self):
        i = 0
        parent = Stack()

        dirname = os.path.dirname(os.path.realpath(__file__))
        proc = subprocess.Popen(['sh', os.path.join(dirname, 'run_cflow.py'), self.source_dir],
                                stdout=subprocess.PIPE)

        while True:
            line = proc.stdout.readline().decode(encoding='UTF-8')

            if line == '':
                break

            current = Call(line)

            if i != 0:
                if current.level > previous.level:
                    parent.push(previous)
                elif current.level < previous.level:
                    for t in range(previous.level - current.level):
                        parent.pop()

                self.call_graph.add_edge(parent.top, current)

            previous = current
            i += 1

    def save_png(self):
        nx.draw(self.call_graph)
        plt.savefig(os.path.basename(os.path.normpath(self.source_dir)) + ".png")

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

    def _select_nodes(self, predicate):
        return [n for n in self.call_graph.nodes() if predicate(n)]