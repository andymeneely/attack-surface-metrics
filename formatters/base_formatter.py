__author__ = 'kevin'


class BaseFormatter(object):
    """
        Formatters' base class.

        Defines interface and provides various methods for extracting metrics from CallGraph objects
        to derived classes.

        Attributes:
            call_graph: The CallGraph object form which to extract the metrics.
    """

    def __init__(self, call_graph):
        """
            Constructor for BaseFormatter
        """
        self.call_graph = call_graph

    def write_output(self):
        """
            When overridden by other classes, generates a text representation of the
            metrics extracted from a Call Graph.
        """
        pass

    def write_summary(self):
        """

        Args:
            self

        Returns:

        """
        pass

    @property
    def source(self):
        # TODO: Fix this documentation
        """
            Returns a string representation of the root directory of the source code analyzed in the Call Graph.
        """
        return self.call_graph.source

    @property
    def nodes_count(self):
        """
            Returns a string representation of the number of nodes present in the Call Graph.
        """
        return str(len(self.call_graph.nodes))

    @property
    def nodes(self):
        """
            Returns all the nodes present in the Call Graph.

            Returns:
                A list of Call objects that represent every function call found in the Call Graph.
        """
        return self.call_graph.nodes

    @property
    def edges_count(self):
        """
            Returns a string representation of the number of edges present in the Call Graph.
        """
        return str(len(self.call_graph.edges))

    @property
    def edges(self):
        """
            Returns all the edges present in the Call Graph.

            Returns:
                A list of 2-tuples of Call objects that represent every caller-callee pair found in the Call Graph.
        """
        return self.call_graph.edges

    @property
    def entry_points_count(self):
        """
            Returns a string representation of the number of Entry Points present in the Call Graph.
        """
        return str(len(self.call_graph.entry_points))

    @property
    def entry_points(self):
        """
            Returns all the Entry Points present in the Call Graph.

            Returns:
                A list of Call objects that represent every Entry Point found in the Call Graph.
        """
        return self.call_graph.entry_points
    
    @property
    def exit_points_count(self):
        """
            Returns a string representation of the number of Exit Points present in the Call Graph.
        """
        return str(len(self.call_graph.exit_points))

    @property
    def exit_points(self):
        """
            Returns all the Exit Points present in the Call Graph.

            Returns:
                A list of Call objects that represent every Exit Point found in the Call Graph.
        """
        return self.call_graph.exit_points

    @property
    def execution_paths_count(self):
        """
            Returns a string representation of the number of Execution Paths present in the Call Graph.
        """
        return str(len(self.call_graph.execution_paths))

    @property
    def average_execution_path_length(self):
        """
            Returns a string representation of the average of Execution Paths length present in the Call Graph.
        """
        return str(self.call_graph.avg_execution_path_length)

    @property
    def median_execution_path_length(self):
        """
            Returns a string representation of the median of Execution Paths length present in the Call Graph.
        """
        return str(self.call_graph.median_execution_path_length)

    @property
    def execution_paths(self):
        """
            Returns all the Exit Points present in the Call Graph.

            Returns:
                A list of lists of Call objects that represent every Execution Path found in the Call Graph.
        """
        return self.call_graph.execution_paths

    @property
    def entry_points_clustering(self):
        """
            Returns a string representation of the clustering of Entry Points present in the Call Graph.
        """
        return str(self.call_graph.entry_points_clustering)

    @property
    def exit_points_clustering(self):
        """
            Returns a string representation of the clustering of Exit Points present in the Call Graph.
        """
        return str(self.call_graph.exit_points_clustering)

    def get_closeness(self, call=None):
        """
            If call is provided, returns a string representation of the closeness of call. If not, returns a list
            of 2-tuples of call-closeness value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the closeness
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_closeness(call))
        else:
            return self.call_graph.get_closeness().items()

    @property
    def average_closeness(self):
        return str(self.call_graph.average_closeness)

    @property
    def median_closeness(self):
        return str(self.call_graph.median_closeness)

    def get_betweenness(self, call=None):
        """
            If call is provided, returns a string representation of the betweenness of call. If not, returns a list
            of 2-tuples of call-betweenness value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the betweenness
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_betweenness(call))
        else:
            return self.call_graph.get_betweenness().items()

    @property
    def average_betweenness(self):
        return str(self.call_graph.average_betweenness)

    @property
    def median_betweenness(self):
        return str(self.call_graph.median_betweenness)

    def get_degree_centrality(self, call=None):
        """
            If call is provided, returns a string representation of the degree centrality of call. If not,
            returns a list of 2-tuples of call-degree centrality value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the degree centrality
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_degree_centrality(call))
        else:
            return self.call_graph.get_degree_centrality().items()

    @property
    def average_degree_centrality(self):
        return str(self.call_graph.average_degree_centrality)

    @property
    def median_degree_centrality(self):
        return str(self.call_graph.median_degree_centrality)

    def get_in_degree_centrality(self, call=None):
        """
            If call is provided, returns a string representation of the in degree centrality of call. If not,
            returns a list of 2-tuples of call-in degree centrality value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the in degree centrality
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_in_degree_centrality(call))
        else:
            return self.call_graph.get_in_degree_centrality().items()

    @property
    def average_in_degree_centrality(self):
        return str(self.call_graph.average_in_degree_centrality)

    @property
    def median_in_degree_centrality(self):
        return str(self.call_graph.median_in_degree_centrality)

    def get_out_degree_centrality(self, call=None):
        """
            If call is provided, returns a string representation of the out degree centrality of call. If not,
            returns a list of 2-tuples of call-out degree centrality value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the out degree centrality
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_out_degree_centrality(call))
        else:
            return self.call_graph.get_out_degree_centrality().items()

    @property
    def average_out_degree_centrality(self):
        return str(self.call_graph.average_out_degree_centrality)

    @property
    def median_out_degree_centrality(self):
        return str(self.call_graph.median_out_degree_centrality)

    def get_degree(self, call=None):
        """
            If call is provided, returns a string representation of the degree of call. If not,
            returns a list of 2-tuples of call-degree value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the degree
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_degree(call))
        else:
            return self.call_graph.get_degree().items()

    @property
    def average_degree(self):
        return str(self.call_graph.average_degree)

    @property
    def median_degree(self):
        return str(self.call_graph.median_degree)

    def get_in_degree(self, call=None):
        """
            If call is provided, returns a string representation of the in degree of call. If not,
            returns a list of 2-tuples of call-in degree value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the in degree
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_in_degree(call))
        else:
            return self.call_graph.get_in_degree().items()

    @property
    def average_in_degree(self):
        return str(self.call_graph.average_in_degree)

    @property
    def median_in_degree(self):
        return str(self.call_graph.median_in_degree)

    def get_out_degree(self, call=None):
        """
            If call is provided, returns a string representation of the out degree of call. If not,
            returns a list of 2-tuples of call-out degree value pairs for every call in the Call Graph.

            Args:
                call: An optional instance of Call representing the call for which the out degree
                is going to be extracted.
        """
        if call:
            return str(self.call_graph.get_out_degree(call))
        else:
            return self.call_graph.get_out_degree().items()

    @property
    def average_out_degree(self):
        return str(self.call_graph.average_out_degree)

    @property
    def median_out_degree(self):
        return str(self.call_graph.median_out_degree)

    def get_descendants_entry_point_ratio(self, call):
        """
            Returns a string representation of the descendants Entry Point ratio of a given Call.
        """
        return str(self.call_graph.get_descendants_entry_point_ratio(call))

    def get_descendants_exit_point_ratio(self, call):
        """
            Returns a string representation of the descendants Exit Point ratio of a given Call.
        """
        return str(self.call_graph.get_descendants_exit_point_ratio(call))

    def get_ancestors_entry_point_ratio(self, call):
        """
            Returns a string representation of the ancestors Entry Point ratio of a given Call.
        """
        return str(self.call_graph.get_ancestors_entry_point_ratio(call))

    def get_ancestors_exit_point_ratio(self, call):
        """
            Returns a string representation of the ancestors Exit Point ratio of a given Call.
        """
        return str(self.call_graph.get_ancestors_exit_point_ratio(call))

    def get_descendant_entry_points_count(self, call):
        """
            Returns a string representation of the number of descendants of a given Call that are Entry Points.
        """
        return str(len(self.call_graph.get_descendant_entry_points(call)))

    def get_descendant_exit_points_count(self, call):
        """
            Returns a string representation of the number of descendants of a given Call that are Exit Points.
        """
        return str(len(self.call_graph.get_descendant_exit_points(call)))

    def get_ancestor_entry_points_count(self, call):
        """
            Returns a string representation of the number of ancestors of a given Call that are Entry Points.
        """
        return str(len(self.call_graph.get_ancestor_entry_points(call)))

    def get_ancestor_exit_points_count(self, call):
        """
            Returns a string representation of the number of ancestors of a given Call that are Exit Points.
        """
        return str(len(self.call_graph.get_ancestor_exit_points(call)))

    def get_descendant_entry_points(self, call):
        """
            Returns all the descendants of a given Call that are Entry Points.

            Returns:
                A list of Call objects that represent all the descendants of a given Call that are Entry Points.
        """
        return self.call_graph.get_descendant_entry_points(call)

    def get_descendant_exit_points(self, call):
        """
            Returns all the descendants of a given Call that are Exit Points.

            Returns:
                A list of Call objects that represent all the descendants of a given Call that are Exit Points.
        """
        return self.call_graph.get_descendant_exit_points(call)

    def get_ancestor_entry_points(self, call):
        """
            Returns all the ancestors of a given Call that are Entry Points.

            Returns:
                A list of Call objects that represent all the ancestors of a given Call that are Entry Points.
        """
        return self.call_graph.get_ancestor_entry_points(call)

    def get_ancestor_exit_points(self, call):
        """
            Returns all the ancestors of a given Call that are Exit Points.

            Returns:
                A list of Call objects that represent all the ancestors of a given Call that are Exit Points.
        """
        return self.call_graph.get_ancestor_exit_points(call)
