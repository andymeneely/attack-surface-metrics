__author__ = 'kevin'

import sys
from attacksurfacemeter import CallGraph
import argparse


def main():
    args = parse_args()

    call_graph = CallGraph(args.source_dir, args.reverse)

    if args.format == "txt":
        output_as_txt(call_graph)




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


def output_as_txt(call_graph):
    print("Attack surface report")
    print("=====================")
    print()
    print("Source code directory: " + call_graph.source_dir)
    print()

    print("Nodes")
    print("=====================")
    print()
    print("Number of nodes: " + str(len(call_graph.nodes)))
    nodes = ', '.join([c.function_name for c in call_graph.nodes])
    print("Nodes:")
    print(nodes)
    print()

    print("Edges")
    print("=====================")
    print()
    print("Number of edges: " + str(len(call_graph.edges)))
    edges = '\n'.join([f.function_name + " ---> " + t.function_name for (f, t) in call_graph.edges])
    print("Edges:")
    print(edges)
    print()

    print("Entry Points")
    print("=====================")
    print()
    print("Number of Entry Points: " + str(len(call_graph.entry_points)))
    print()
    entry_points = ', '.join([c.function_name for c in call_graph.entry_points])
    print("Entry Points:")
    print(entry_points)
    print()

    print("Exit Points")
    print("=====================")
    print()
    print("Number of Exit Points: " + str(len(call_graph.exit_points)))
    print()
    exit_points = ', '.join([c.function_name for c in call_graph.exit_points])
    print("Exit Points:")
    print(exit_points)
    print()

    print("Execution Paths")
    print("=====================")
    print()
    print("Number of Execution Paths: " + str(len(call_graph.execution_paths)))
    print()
    execution_paths = '\n'.join([' ---> '.join(c.function_name for c in p) for p in call_graph.execution_paths])
    print("Execution Paths:")
    print(execution_paths)
    print()
    print("Average Execution Path Length: " + str(call_graph.avg_execution_path_length))
    print("Median Execution Path Length: " + str(call_graph.median_execution_path_length))

    print("Clustering")
    print("=====================")
    print()
    print("Average Entry Point Clustering: " + str(call_graph.entry_points_clustering))
    print("Average Exit Point Clustering: " + str(call_graph.exit_points_clustering))


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