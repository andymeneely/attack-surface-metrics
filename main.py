__author__ = 'kevin'

import sys

from attack_surface import CallGraph


def main(args):
    source_dir = args[1]

    call_graph = CallGraph(source_dir)

    print("entry points: " + str(len(call_graph.entry_points)))
    print("exit points: " + str(len(call_graph.exit_points)))

if __name__ == '__main__':
    main(sys.argv)