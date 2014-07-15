__author__ = 'kevin'

import sys
from attacksurfacemeter import CallGraph
import argparse


def main():
    args = parse_args()

    call_graph = CallGraph(args.source_dir, args.reverse)

    if args.format == "txt":
        formatter = TxtFormatter(call_graph)

    formatter.write_output()


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


class BaseFormatter(object):

    def __init__(self, call_graph):
        """Constructor for BaseFormatter"""
        self.call_graph = call_graph

    # def write_output(self, call_graph):
    #     """
    #
    #     Args:
    #         call_graph
    #
    #     Returns:
    #
    #     """
    #     self.write_header(call_graph)
    #     self.write_nodes(call_graph)
    #     self.write_edges(call_graph)
    #     self.write_entry_points(call_graph)
    #     self.write_exit_points(call_graph)
    #     self.write_execution_paths(call_graph)
    #     self.write_closeness(call_graph)
    #     self.write_betweenness(call_graph)
    #     self.write_clustering(call_graph)
    #     self.write_degree_centrality(call_graph)
    #     self.write_in_degree_centrality(call_graph)
    #     self.write_out_degree_centrality(call_graph)
    #     self.write_degree(call_graph)
    #     self.write_in_degree(call_graph)
    #     self.write_out_degree(call_graph)
    #     self.write_descendant_entry_points(call_graph)
    #     self.write_descendant_exit_points(call_graph)
    #     self.write_ancestor_entry_points(call_graph)
    #     self.write_ancestor_exit_points(call_graph)
    #     self.write_descendant_entry_points_ratio(call_graph)
    #     self.write_descendant_exit_points_ratio(call_graph)
    #     self.write_ancestor_entry_points_ratio(call_graph)
    #     self.write_ancestor_exit_points_ratio(call_graph)
    #
    # def write_header(self):
    #     pass
    #
    # def write_nodes(self):
    #     pass
    #
    # def write_edges(self):
    #     pass
    #
    # def write_entry_points(self):
    #     pass
    #
    # def write_exit_points(self):
    #     pass
    #
    # def write_execution_paths(self):
    #     pass
    #
    # def write_closeness(self):
    #     pass
    #
    # def write_betweenness(self):
    #     pass
    #
    # def write_clustering(self):
    #     pass
    #
    # def write_degree_centrality(self):
    #     pass
    #
    # def write_in_degree_centrality(self):
    #     pass
    #
    # def write_out_degree_centrality(self):
    #     pass
    #
    # def write_degree(self):
    #     pass
    #
    # def write_in_degree(self):
    #     pass
    #
    # def write_out_degree(self):
    #     pass
    #
    # def write_descendant_entry_points(self):
    #     pass
    #
    # def write_descendant_exit_points(self):
    #     pass
    #
    # def write_ancestor_entry_points(self):
    #     pass
    #
    # def write_ancestor_exit_points(self):
    #     pass
    #
    # def write_descendant_entry_points_ratio(self):
    #     pass
    #
    # def write_descendant_exit_points_ratio(self):
    #     pass
    #
    # def write_ancestor_entry_points_ratio(self):
    #     pass
    #
    # def write_ancestor_exit_points_ratio(self):
    #     pass


class TxtFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(TxtFormatter, self).__init__(call_graph)

    def write_output(self):
        print("Attack surface report")
        print("=====================")
        print()
        print("Source code directory: " + self.call_graph.source_dir)
        print()

        print("Nodes")
        print("=====================")
        print()
        print("Number of nodes: " + str(len(self.call_graph.nodes)))
        nodes = ', '.join([c.function_name for c in self.call_graph.nodes])
        print("Nodes:")
        print(nodes)
        print()

        print("Edges")
        print("=====================")
        print()
        print("Number of edges: " + str(len(self.call_graph.edges)))
        edges = '\n'.join([f.function_name + " ---> " + t.function_name for (f, t) in self.call_graph.edges])
        print("Edges:")
        print(edges)
        print()

        print("Entry Points")
        print("=====================")
        print()
        print("Number of Entry Points: " + str(len(self.call_graph.entry_points)))
        print()
        entry_points = ', '.join([c.function_name for c in self.call_graph.entry_points])
        print("Entry Points:")
        print(entry_points)
        print()

        print("Exit Points")
        print("=====================")
        print()
        print("Number of Exit Points: " + str(len(self.call_graph.exit_points)))
        print()
        exit_points = ', '.join([c.function_name for c in self.call_graph.exit_points])
        print("Exit Points:")
        print(exit_points)
        print()

        print("Execution Paths")
        print("=====================")
        print()
        print("Number of Execution Paths: " + str(len(self.call_graph.execution_paths)))
        print()
        execution_paths = '\n'.join([' ---> '.join(c.function_name for c in p) for p in self.call_graph.execution_paths])
        print("Execution Paths:")
        print(execution_paths)
        print()
        print("Average Execution Path Length: " + str(self.call_graph.avg_execution_path_length))
        print("Median Execution Path Length: " + str(self.call_graph.median_execution_path_length))
        print()

        print("Closeness")
        print("=====================")
        print()
        closeness = "\n".join([k.function_name + ": " + str(v)
                               for k, v in self.call_graph.get_closeness().items()])
        print(closeness)
        print()

        print("Betweenness")
        print("=====================")
        print()
        betweenness = "\n".join([k.function_name + ": " + str(v)
                                 for k, v in self.call_graph.get_betweenness().items()])
        print(betweenness)
        print()

        print("Clustering")
        print("=====================")
        print()
        print("Average Entry Point Clustering: " + str(self.call_graph.entry_points_clustering))
        print("Average Exit Point Clustering: " + str(self.call_graph.exit_points_clustering))
        print()

        print("Degree Centrality")
        print("=====================")
        print()
        centrality = "\n".join([k.function_name + ": " + str(v)
                                for k, v in self.call_graph.get_degree_centrality().items()])
        print(centrality)
        print()

        print("In Degree Centrality")
        print("=====================")
        print()
        in_centrality = "\n".join([k.function_name + ": " + str(v)
                                   for k, v in self.call_graph.get_in_degree_centrality().items()])
        print(in_centrality)
        print()

        print("Out Degree Centrality")
        print("=====================")
        print()
        out_centrality = "\n".join([k.function_name + ": " + str(v)
                                    for k, v in self.call_graph.get_out_degree_centrality().items()])
        print(out_centrality)
        print()

        print("Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.call_graph.get_degree().items()])
        print(degree)
        print()

        print("In Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.call_graph.get_in_degree().items()])
        print(degree)
        print()

        print("Out Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.call_graph.get_out_degree().items()])
        print(degree)
        print()

        # print("Descendants")
        # print("=====================")
        # print()
        # descendants = "\n".join([c.function_name + ": " +
        #                          ", ".join([d.function_name
        #                                     for d in self.call_graph.get_descendants(c)])
        #                          for c in self.call_graph.nodes
        #                          if len(self.call_graph.get_descendants(c)) > 0])
        # print(descendants)
        # print()

        print("Descendant Entry Points")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 ", ".join([d.function_name
                                            for d in self.call_graph.get_descendant_entry_points(c)])
                                 for c in self.call_graph.nodes
                                 if len(self.call_graph.get_descendant_entry_points(c)) > 0])
        print(descendants)
        print()

        print("Descendant Exit Points")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 ", ".join([d.function_name
                                            for d in self.call_graph.get_descendant_exit_points(c)])
                                 for c in self.call_graph.nodes
                                 if len(self.call_graph.get_descendant_exit_points(c)) > 0])
        print(descendants)
        print()

        # print("Ancestors")
        # print("=====================")
        # print()
        # ancestors = "\n".join([c.function_name + ": " +
        #                        ", ".join([d.function_name
        #                                   for d in self.call_graph.get_ancestors(c)])
        #                        for c in self.call_graph.nodes
        #                        if len(self.call_graph.get_ancestors(c)) > 0])
        # print(ancestors)
        # print()

        print("Ancestor Entry Points")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               ", ".join([d.function_name
                                          for d in self.call_graph.get_ancestor_entry_points(c)])
                               for c in self.call_graph.nodes
                               if len(self.call_graph.get_ancestor_entry_points(c)) > 0])
        print(ancestors)
        print()

        print("Ancestor Exit Points")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               ", ".join([d.function_name
                                          for d in self.call_graph.get_ancestor_exit_points(c)])
                               for c in self.call_graph.nodes
                               if len(self.call_graph.get_ancestor_exit_points(c)) > 0])
        print(ancestors)
        print()

        print("Descendant Entry Points Ratio")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.call_graph.get_descendants_entry_point_ratio(c))
                                 for c in self.call_graph.nodes])
        print(descendants)
        print()

        print("Descendant Exit Points Ratio")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.call_graph.get_descendants_exit_point_ratio(c))
                                 for c in self.call_graph.nodes])
        print(descendants)
        print()

        print("Ancestor Entry Points Ratio")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.call_graph.get_ancestors_entry_point_ratio(c))
                               for c in self.call_graph.nodes])

        print(ancestors)
        print()

        print("Ancestor Exit Points Ratio")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.call_graph.get_ancestors_exit_point_ratio(c))
                               for c in self.call_graph.nodes])
        print(ancestors)
        print()


class HtmlFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(BaseFormatter, self).__init__(call_graph)


class XmlFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(BaseFormatter, self).__init__(call_graph)


class JsonFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(BaseFormatter, self).__init__(call_graph)


if __name__ == '__main__':
    main()