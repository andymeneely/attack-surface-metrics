__author__ = 'kevin'

import sys

from attacksurfacemeter import CallGraph


def main(args):
    source_dir = args[1]

    call_graph = CallGraph(source_dir)

    print("nodes: " + str(len(call_graph.nodes)))
    print("edges: " + str(len(call_graph.edges)))

    print("entry points: " + str(len(call_graph.entry_points)))
    print("exit points: " + str(len(call_graph.exit_points)))

    print("execution paths: " + str(len(call_graph.execution_paths)))
    print("average execution path length: " + str(call_graph.avg_execution_path_length))
    print("median execution path length: " + str(call_graph.median_execution_path_length))

    print("average entry point clustering: " + str(call_graph.entry_points_clustering))
    print("average exit point clustering: " + str(call_graph.exit_points_clustering))

if __name__ == '__main__':
    main(sys.argv)