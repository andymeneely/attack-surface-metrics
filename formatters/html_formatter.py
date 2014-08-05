__author__ = 'kevin'

import os

from django.template import Template, Context
from django.conf import settings

from formatters.base_formatter import BaseFormatter


class HtmlFormatter(BaseFormatter):

    def __init__(self, call_graph):
        super(HtmlFormatter, self).__init__(call_graph)

    @staticmethod
    def _get_template():
        template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template.html")
        settings.configure()

        return Template(open(template_file, 'r').read())

    @staticmethod
    def _get_signature(call):
        return '' if call.function_signature is None else call.function_signature

    @staticmethod
    def _transform_calls(calls):
        return [{'function_name': c.function_name,
                 'function_signature': HtmlFormatter._get_signature}
                for c in calls]

    def write_output(self):
        template = HtmlFormatter._get_template()

        context = Context({
            'directory': self.source_dir,
            'nodes_count': self.nodes_count,
            'nodes': [{
                          'function_name': c.function_name,
                          'function_signature': HtmlFormatter._get_signature(c),
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
                          'descendant_entry_points': HtmlFormatter._transform_calls(self.get_descendant_entry_points(c)),

                          'descendant_exit_points_count': self.get_descendant_exit_points_count(c),
                          'descendant_exit_points': HtmlFormatter._transform_calls(self.get_descendant_exit_points(c)),

                          'ancestor_entry_points_count': self.get_ancestor_entry_points_count(c),
                          'ancestor_entry_points': HtmlFormatter._transform_calls(self.get_ancestor_entry_points(c)),

                          'ancestor_exit_points_count': self.get_ancestor_exit_points_count(c),
                          'ancestor_exit_points': HtmlFormatter._transform_calls(self.get_ancestor_exit_points(c))}
                      for c in self.nodes],

            'edges_count': self.edges_count,
            'edges': [{'from': f.function_name,
                       'to': t.function_name}
                      for (f, t) in self.edges],

            'entry_points_count': self.entry_points_count,
            'entry_points': HtmlFormatter._transform_calls(self.entry_points),

            'exit_points_count': self.exit_points_count,
            'exit_points': HtmlFormatter._transform_calls(self.exit_points),

            'entry_points_clustering': self.entry_points_clustering,
            'exit_points_clustering': self.exit_points_clustering,

            'execution_paths_count': self.execution_paths_count,
            'execution_paths_average': self.average_execution_path_length,
            'execution_paths_median': self.median_execution_path_length,

            'execution_paths': [{'length': str(len(xp)),
                                 'path': HtmlFormatter._transform_calls(xp)}
                                for xp in self.execution_paths]
        })

        return template.render(context)