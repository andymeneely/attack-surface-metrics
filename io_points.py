__author__ = 'kevin'

import sys
import subprocess
import os

import networkx as nx
import matplotlib.pyplot as plt

from stack import Stack
from call import Call

def main(args):
    source_dir = args[1]

    entry_points = list()
    exit_points = list()
    entry_points_count = 0
    exit_points_count = 0

    call_graph = nx.DiGraph()
    parent = Stack()
    i = 0

    proc = subprocess.Popen(['sh', 'run_cflow.sh', source_dir], stdout=subprocess.PIPE)

    while True:
        line = proc.stdout.readline().decode(encoding='UTF-8')

        if line == '':
            break

        print(str(i) + ":\t" + line.rstrip())
        current = Call(line)

        if i != 0:
            if current.level > previous.level:
                parent.push(previous)
            elif current.level < previous.level:
                for t in range(previous.level - current.level):
                    parent.pop()

            call_graph.add_edge(parent.top, current)

            if current.is_input_function():
                entry_points.append(parent.top)
                # entry_points_count += 1
            if current.is_output_function():
                exit_points.append(parent.top)
                # exit_points_count += 1

        previous = current
        i += 1

    # print("entry points: " + str(entry_points_count))
    # print("exit points: " + str(exit_points_count))

    print("entry points: " + str(len(entry_points)))
    print("exit points: " + str(len(exit_points)))

    print("entry points: " + str(len(set(entry_points))))
    print("exit points: " + str(len(set(exit_points))))

    nx.draw(call_graph)
    plt.savefig(os.path.basename(os.path.normpath(source_dir)) + ".png")


if __name__ == '__main__':
    main(sys.argv)