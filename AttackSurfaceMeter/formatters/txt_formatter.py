__author__ = 'kevin'

from formatters.base_formatter import BaseFormatter


class TxtFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(TxtFormatter, self).__init__(call_graph)

    def write_output(self):
        print("Attack surface report")
        print("=====================")
        print()
        print("Source code directory: " + self.source_dir)
        print()

        print("Nodes")
        print("=====================")
        print()
        print("Number of nodes: " + self.nodes_count)
        nodes = ', '.join([c.function_name for c in self.nodes])
        print("Nodes:")
        print(nodes)
        print()

        print("Edges")
        print("=====================")
        print()
        print("Number of edges: " + self.edges_count)
        edges = '\n'.join([f.function_name + " ---> " + t.function_name for (f, t) in self.edges])
        print("Edges:")
        print(edges)
        print()

        print("Entry Points")
        print("=====================")
        print()
        print("Number of Entry Points: " + self.entry_points_count)
        print()
        entry_points = ', '.join([c.function_name for c in self.entry_points])
        print("Entry Points:")
        print(entry_points)
        print()

        print("Exit Points")
        print("=====================")
        print()
        print("Number of Exit Points: " + self.exit_points_count)
        print()
        exit_points = ', '.join([c.function_name for c in self.exit_points])
        print("Exit Points:")
        print(exit_points)
        print()

        print("Execution Paths")
        print("=====================")
        print()
        print("Number of Execution Paths: " + self.execution_paths_count)
        print()
        execution_paths = '\n'.join([' ---> '.join(c.function_name for c in p) for p in self.execution_paths])
        print("Execution Paths:")
        print(execution_paths)
        print()
        print("Average Execution Path Length: " + self.average_execution_path_length)
        print("Median Execution Path Length: " + self.median_execution_path_length)
        print()

        print("Closeness")
        print("=====================")
        print()
        closeness = "\n".join([k.function_name + ": " + str(v)
                               for k, v in self.get_closeness()])
        print(closeness)
        print()

        print("Betweenness")
        print("=====================")
        print()
        betweenness = "\n".join([k.function_name + ": " + str(v)
                                 for k, v in self.get_betweenness()])
        print(betweenness)
        print()

        print("Clustering")
        print("=====================")
        print()
        print("Average Entry Point Clustering: " + self.entry_points_clustering)
        print("Average Exit Point Clustering: " + self.exit_points_clustering)
        print()

        print("Degree Centrality")
        print("=====================")
        print()
        centrality = "\n".join([k.function_name + ": " + str(v)
                                for k, v in self.get_degree_centrality()])
        print(centrality)
        print()

        print("In Degree Centrality")
        print("=====================")
        print()
        in_centrality = "\n".join([k.function_name + ": " + str(v)
                                   for k, v in self.get_in_degree_centrality()])
        print(in_centrality)
        print()

        print("Out Degree Centrality")
        print("=====================")
        print()
        out_centrality = "\n".join([k.function_name + ": " + str(v)
                                    for k, v in self.get_out_degree_centrality()])
        print(out_centrality)
        print()

        print("Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_degree()])
        print(degree)
        print()

        print("In Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_in_degree()])
        print(degree)
        print()

        print("Out Degree")
        print("=====================")
        print()
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_out_degree()])
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
                                            for d in self.get_descendant_entry_points(c)])
                                 for c in self.nodes
                                 if len(self.get_descendant_entry_points(c)) > 0])
        print(descendants)
        print()

        print("Descendant Exit Points")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 ", ".join([d.function_name
                                            for d in self.get_descendant_exit_points(c)])
                                 for c in self.nodes
                                 if len(self.get_descendant_exit_points(c)) > 0])
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
                                          for d in self.get_ancestor_entry_points(c)])
                               for c in self.nodes
                               if len(self.get_ancestor_entry_points(c)) > 0])
        print(ancestors)
        print()

        print("Ancestor Exit Points")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               ", ".join([d.function_name
                                          for d in self.get_ancestor_exit_points(c)])
                               for c in self.nodes
                               if len(self.get_ancestor_exit_points(c)) > 0])
        print(ancestors)
        print()

        print("Descendant Entry Points Ratio")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.get_descendants_entry_point_ratio(c))
                                 for c in self.nodes])
        print(descendants)
        print()

        print("Descendant Exit Points Ratio")
        print("=====================")
        print()
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.get_descendants_exit_point_ratio(c))
                                 for c in self.nodes])
        print(descendants)
        print()

        print("Ancestor Entry Points Ratio")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.get_ancestors_entry_point_ratio(c))
                               for c in self.nodes])

        print(ancestors)
        print()

        print("Ancestor Exit Points Ratio")
        print("=====================")
        print()
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.get_ancestors_exit_point_ratio(c))
                               for c in self.nodes])
        print(ancestors)
        print()
