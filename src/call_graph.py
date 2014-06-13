__author__ = 'kevin'

import subprocess
import os

import networkx as nx
import matplotlib.pyplot as plt

from stack import Stack
from call import Call


class CallGraph():

    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.call_graph = nx.DiGraph()

        self.entry_points = set()
        self.exit_points = set()

        self.generate()

    def generate(self):
        i = 0
        parent = Stack()
        proc = subprocess.Popen(['sh', 'run_cflow.sh', self.source_dir], stdout=subprocess.PIPE)

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

                if current.is_input_function():
                    self.entry_points.add(parent.top)
                if current.is_output_function():
                    self.exit_points.add(parent.top)

            previous = current
            i += 1

    def save_png(self):
        nx.draw(self.call_graph)
        plt.savefig(os.path.basename(os.path.normpath(self.source_dir)) + ".png")