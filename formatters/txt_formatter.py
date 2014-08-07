__author__ = 'kevin'

from formatters.base_formatter import BaseFormatter


class TxtFormatter(BaseFormatter):
    """
        Produces a plain text report with the attack surface metrics calculated by call_graph
        and prints it to console.
    """
    def __init__(self, call_graph):
        super(TxtFormatter, self).__init__(call_graph)

    def write_summary(self):
        output = ''

        output += "Attack surface report summary\n"
        output += "=====================\n"
        output += "\n"
        output += "Source code directory: " + self.source_dir + "\n"
        output += "Number of nodes: " + self.nodes_count + "\n"
        output += "Number of edges: " + self.edges_count + "\n"
        output += "Number of Entry Points: " + self.entry_points_count + "\n"
        output += "Number of Exit Points: " + self.exit_points_count + "\n"
        output += "Number of Execution Paths: " + self.execution_paths_count + "\n"
        output += "Average Execution Path Length: " + self.average_execution_path_length + "\n"
        output += "Median Execution Path Length: " + self.median_execution_path_length + "\n"
        output += "Average Closeness: " + self.average_closeness + "\n"
        output += "Median Closeness: " + self.median_closeness + "\n"
        output += "Average Betweenness: " + self.average_betweenness + "\n"
        output += "Median Betweenness: " + self.median_betweenness + "\n"
        output += "Average Entry Point Clustering: " + self.entry_points_clustering + "\n"
        output += "Average Exit Point Clustering: " + self.exit_points_clustering + "\n"
        output += "Average Degree Centrality: " + self.average_degree_centrality + "\n"
        output += "Median Degree Centrality: " + self.median_degree_centrality + "\n"
        output += "Average In Degree Centrality: " + self.average_in_degree_centrality + "\n"
        output += "Median In Degree Centrality: " + self.median_in_degree_centrality + "\n"
        output += "Average Out Degree Centrality: " + self.average_out_degree_centrality + "\n"
        output += "Median Out Degree Centrality: " + self.median_out_degree_centrality + "\n"
        output += "Average Degree: " + self.average_degree + "\n"
        output += "Median Degree: " + self.median_degree + "\n"
        output += "Average In Degree: " + self.average_in_degree + "\n"
        output += "Median In Degree: " + self.median_in_degree + "\n"
        output += "Average Out Degree: " + self.average_out_degree + "\n"
        output += "Median Out Degree: " + self.median_out_degree + "\n"

        return output

    def write_output(self):
        output = ''
        
        output += "Attack surface report\n"
        output += "=====================\n"
        output += "\n"
        output += "Source code directory: " + self.source_dir + "\n"
        output += "\n"

        output += "Nodes\n"
        output += "=====================\n"
        output += "\n"
        output += "Number of nodes: " + self.nodes_count + "\n"
        nodes = ', '.join([c.function_name for c in self.nodes])
        output += "Nodes:\n"
        output += nodes + "\n"
        output += "\n"

        output += "Edges\n"
        output += "=====================\n"
        output += "\n"
        output += "Number of edges: " + self.edges_count + "\n"
        edges = '\n'.join([f.function_name + " ---> " + t.function_name for (f, t) in self.edges])
        output += "Edges:\n"
        output += edges + "\n"
        output += "\n"

        output += "Entry Points\n"
        output += "=====================\n"
        output += "\n"
        output += "Number of Entry Points: " + self.entry_points_count + "\n"
        output += "\n"
        entry_points = ', '.join([c.function_name for c in self.entry_points])
        output += "Entry Points:\n"
        output += entry_points + "\n"
        output += "\n"

        output += "Exit Points\n"
        output += "=====================\n"
        output += "\n"
        output += "Number of Exit Points: " + self.exit_points_count + "\n"
        output += "\n"
        exit_points = ', '.join([c.function_name for c in self.exit_points])
        output += "Exit Points:\n"
        output += exit_points + "\n"
        output += "\n"

        output += "Execution Paths\n"
        output += "=====================\n"
        output += "\n"
        output += "Number of Execution Paths: " + self.execution_paths_count + "\n"
        output += "\n"
        execution_paths = '\n'.join([' ---> '.join(c.function_name for c in p) for p in self.execution_paths])
        output += "Execution Paths:\n"
        output += execution_paths + "\n"
        output += "\n"
        output += "Average Execution Path Length: " + self.average_execution_path_length + "\n"
        output += "Median Execution Path Length: " + self.median_execution_path_length + "\n"
        output += "\n"

        output += "Closeness\n"
        output += "=====================\n"
        output += "\n"
        closeness = "\n".join([k.function_name + ": " + str(v)
                               for k, v in self.get_closeness()])
        output += closeness + "\n"
        output += "\n"

        output += "Betweenness\n"
        output += "=====================\n"
        output += "\n"
        betweenness = "\n".join([k.function_name + ": " + str(v)
                                 for k, v in self.get_betweenness()])
        output += betweenness + "\n"
        output += "\n"

        output += "Clustering\n"
        output += "=====================\n"
        output += "\n"
        output += "Average Entry Point Clustering: " + self.entry_points_clustering + "\n"
        output += "Average Exit Point Clustering: " + self.exit_points_clustering + "\n"
        output += "\n"

        output += "Degree Centrality\n"
        output += "=====================\n"
        output += "\n"
        centrality = "\n".join([k.function_name + ": " + str(v)
                                for k, v in self.get_degree_centrality()])
        output += centrality + "\n"
        output += "\n"

        output += "In Degree Centrality\n"
        output += "=====================\n"
        output += "\n"
        in_centrality = "\n".join([k.function_name + ": " + str(v)
                                   for k, v in self.get_in_degree_centrality()])
        output += in_centrality + "\n"
        output += "\n"

        output += "Out Degree Centrality\n"
        output += "=====================\n"
        output += "\n"
        out_centrality = "\n".join([k.function_name + ": " + str(v)
                                    for k, v in self.get_out_degree_centrality()])
        output += out_centrality + "\n"
        output += "\n"

        output += "Degree\n"
        output += "=====================\n"
        output += "\n"
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_degree()])
        output += degree + "\n"
        output += "\n"

        output += "In Degree\n"
        output += "=====================\n"
        output += "\n"
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_in_degree()])
        output += degree + "\n"
        output += "\n"

        output += "Out Degree\n"
        output += "=====================\n"
        output += "\n"
        degree = "\n".join([k.function_name + ": " + str(v)
                            for k, v in self.get_out_degree()])
        output += degree + "\n"
        output += "\n"

        # output += "Descendants\n"
        # output += "=====================\n"
        # output += "\n"
        # descendants = "\n".join([c.function_name + ": " +
        #                          ", ".join([d.function_name
        #                                     for d in self.call_graph.get_descendants(c)])
        #                          for c in self.call_graph.nodes
        #                          if len(self.call_graph.get_descendants(c)) > 0])
        # output += descendants)
        # output += "\n"

        output += "Descendant Entry Points\n"
        output += "=====================\n"
        output += "\n"
        descendants = "\n".join([c.function_name + ": " +
                                 ", ".join([d.function_name
                                            for d in self.get_descendant_entry_points(c)])
                                 for c in self.nodes
                                 if len(self.get_descendant_entry_points(c)) > 0])
        output += descendants + "\n"
        output += "\n"

        output += "Descendant Exit Points\n"
        output += "=====================\n"
        output += "\n"
        descendants = "\n".join([c.function_name + ": " +
                                 ", ".join([d.function_name
                                            for d in self.get_descendant_exit_points(c)])
                                 for c in self.nodes
                                 if len(self.get_descendant_exit_points(c)) > 0])
        output += descendants + "\n"
        output += "\n"

        # output += "Ancestors\n"
        # output += "=====================\n"
        # output += "\n"
        # ancestors = "\n".join([c.function_name + ": " +
        #                        ", ".join([d.function_name
        #                                   for d in self.call_graph.get_ancestors(c)])
        #                        for c in self.call_graph.nodes
        #                        if len(self.call_graph.get_ancestors(c)) > 0])
        # output += ancestors)
        # output += "\n"

        output += "Ancestor Entry Points\n"
        output += "=====================\n"
        output += "\n"
        ancestors = "\n".join([c.function_name + ": " +
                               ", ".join([d.function_name
                                          for d in self.get_ancestor_entry_points(c)])
                               for c in self.nodes
                               if len(self.get_ancestor_entry_points(c)) > 0])
        output += ancestors + "\n"
        output += "\n"

        output += "Ancestor Exit Points\n"
        output += "=====================\n"
        output += "\n"
        ancestors = "\n".join([c.function_name + ": " +
                               ", ".join([d.function_name
                                          for d in self.get_ancestor_exit_points(c)])
                               for c in self.nodes
                               if len(self.get_ancestor_exit_points(c)) > 0])
        output += ancestors + "\n"
        output += "\n"

        output += "Descendant Entry Points Ratio\n"
        output += "=====================\n"
        output += "\n"
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.get_descendants_entry_point_ratio(c))
                                 for c in self.nodes])
        output += descendants + "\n"
        output += "\n"

        output += "Descendant Exit Points Ratio\n"
        output += "=====================\n"
        output += "\n"
        descendants = "\n".join([c.function_name + ": " +
                                 str(self.get_descendants_exit_point_ratio(c))
                                 for c in self.nodes])
        output += descendants + "\n"
        output += "\n"

        output += "Ancestor Entry Points Ratio\n"
        output += "=====================\n"
        output += "\n"
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.get_ancestors_entry_point_ratio(c))
                               for c in self.nodes])

        output += ancestors + "\n"
        output += "\n"

        output += "Ancestor Exit Points Ratio\n"
        output += "=====================\n"
        output += "\n"
        ancestors = "\n".join([c.function_name + ": " +
                               str(self.get_ancestors_exit_point_ratio(c))
                               for c in self.nodes])
        output += ancestors

        return output
