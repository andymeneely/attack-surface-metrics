__author__ = 'kevin'

import sys
from attacksurfacemeter import CallGraph
import argparse


def main():
    args = parse_args()

    source_dir = args.source_dir

    print(args.source_dir)
    print(args.format)
    print(args.output)
    print(args.reverse)

    print("Call Graph\n")
    calculate_metrics(CallGraph(source_dir))

    print("Reversed Call Graph\n")
    calculate_metrics(CallGraph(source_dir, True))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyzes a software's source code and reports various metrics related to it's attack surface.")

    parser.add_argument("source_dir", help="Root directory of the source code to analyze.")
    parser.add_argument("-f", "--format", choices=["txt", "html", "xml", "json"], default="txt",
                        help="Output format of the calculated metrics.")
    parser.add_argument("-o", "--output", help="Output file.", default="output.metrics")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="When using cflow for call graph generation, use the reverse algorithm.")

    return parser.parse_args()


def calculate_metrics(call_graph):
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
    main()