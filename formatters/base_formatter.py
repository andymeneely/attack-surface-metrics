__author__ = 'kevin'

import os
from statistics import StatisticsError

from django.template import Template, Context
from django.conf import settings


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

    @staticmethod
    def _get_template(template_file):
        template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), template_file)

        if not settings.configured:
            settings.configure()

        return Template(open(template_file, 'r').read())

    @staticmethod
    def _get_signature(call):
        return '' if call.function_signature is None else call.function_signature

    @staticmethod
    def _transform_calls(calls):
        return [{'function_name': c.function_name,
                 'function_signature': BaseFormatter._get_signature(c)}
                for c in calls]

    def write_summary(self):
        template = BaseFormatter._get_template(self.summary_template_file)

        context = Context({
            'directory': self.source,

            'nodes_count': self.nodes_count,
            'edges_count': self.edges_count,

            'entry_points_count': self.entry_points_count,
            'exit_points_count': self.exit_points_count,

            'execution_paths_count': self.execution_paths_count,
            'execution_paths_average': self.average_execution_path_length,
            'execution_paths_median': self.median_execution_path_length,

            'average_closeness': self.average_closeness,
            'median_closeness': self.median_closeness,

            'average_betweenness': self.average_betweenness,
            'median_betweenness': self.median_betweenness,

            'entry_points_clustering': self.entry_points_clustering,
            'exit_points_clustering': self.exit_points_clustering,

            'average_degree_centrality': self.average_degree_centrality,
            'median_degree_centrality': self.median_degree_centrality,
            'average_in_degree_centrality': self.average_in_degree_centrality,
            'median_in_degree_centrality': self.median_in_degree_centrality,
            'average_out_degree_centrality': self.average_out_degree_centrality,
            'median_out_degree_centrality': self.median_out_degree_centrality,

            'average_degree': self.average_degree,
            'median_degree': self.median_degree,
            'average_in_degree': self.average_in_degree,
            'median_in_degree': self.median_in_degree,
            'average_out_degree': self.average_out_degree,
            'median_out_degree': self.median_out_degree
        })

        return template.render(context)

    def write_output(self):
        template = BaseFormatter._get_template(self.template_file)

        context = Context({
            'directory': self.source,
            'nodes_count': self.nodes_count,
            'nodes': [{
                          'function_name': c.function_name,
                          'function_signature': BaseFormatter._get_signature(c),
                          'closeness': self.get_closeness(c),
                          'betweenness': self.get_betweenness(c),
                          'degree_centrality': self.get_degree_centrality(c),
                          'in_degree_centrality': self.get_in_degree_centrality(c),
                          'out_degree_centrality': self.get_out_degree_centrality(c),
                          'degree': self.get_degree(c),
                          'in_degree': self.get_in_degree(c),
                          'out_degree': self.get_out_degree(c),
                          'descendant_entry_points_ratio': self.get_descendants_entry_point_ratio(c),
                          'descendant_exit_points_ratio': self.get_descendants_exit_point_ratio(c),
                          'ancestor_entry_points_ratio': self.get_ancestors_entry_point_ratio(c),
                          'ancestor_exit_points_ratio': self.get_ancestors_exit_point_ratio(c),

                          'descendant_entry_points_count': self.get_descendant_entry_points_count(c),
                          'descendant_entry_points': BaseFormatter._transform_calls(self.get_descendant_entry_points(c)),

                          'descendant_exit_points_count': self.get_descendant_exit_points_count(c),
                          'descendant_exit_points': BaseFormatter._transform_calls(self.get_descendant_exit_points(c)),

                          'ancestor_entry_points_count': self.get_ancestor_entry_points_count(c),
                          'ancestor_entry_points': BaseFormatter._transform_calls(self.get_ancestor_entry_points(c)),

                          'ancestor_exit_points_count': self.get_ancestor_exit_points_count(c),
                          'ancestor_exit_points': BaseFormatter._transform_calls(self.get_ancestor_exit_points(c))}
                      for c in self.nodes],

            'edges_count': self.edges_count,
            'edges': [{'from': f.function_name,
                       'to': t.function_name}
                      for (f, t) in self.edges],

            'entry_points_count': self.entry_points_count,
            'entry_points': BaseFormatter._transform_calls(self.entry_points),

            'exit_points_count': self.exit_points_count,
            'exit_points': BaseFormatter._transform_calls(self.exit_points),

            'entry_points_clustering': self.entry_points_clustering,
            'exit_points_clustering': self.exit_points_clustering,

            'execution_paths_count': self.execution_paths_count,
            'execution_paths_average': self.average_execution_path_length,
            'execution_paths_median': self.median_execution_path_length,

            'execution_paths': [{'length': str(len(xp)),
                                 'path': BaseFormatter._transform_calls(xp)}
                                for xp in self.execution_paths]
        })

        return template.render(context)
    
    @property
    def template_file(self):
        pass
    
    @property
    def summary_template_file(self):
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
        try:
            return str(self.call_graph.avg_execution_path_length)
        except StatisticsError as e:
            return "Error: " + str(e)

    @property
    def median_execution_path_length(self):
        """
            Returns a string representation of the median of Execution Paths length present in the Call Graph.
        """
        try:
            return str(self.call_graph.median_execution_path_length)
        except StatisticsError as e:
            return "Error: " + str(e)

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
        try:
            return str(self.call_graph.entry_points_clustering)
        except ZeroDivisionError as e:
            return "Error: " + str(e)

    @property
    def exit_points_clustering(self):
        """
            Returns a string representation of the clustering of Exit Points present in the Call Graph.
        """
        try:
            return str(self.call_graph.exit_points_clustering)
        except ZeroDivisionError as e:
            return "Error: " + str(e)

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
