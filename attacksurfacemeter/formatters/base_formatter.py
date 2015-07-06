import os
from statistics import StatisticsError

import networkx as nx

from django.template import Template, Context
from django.conf import settings


class BaseFormatter(object):
    """Formatters' base class.

     Defines interface and provides various methods for extracting metrics from
     CallGraph objects to derived classes.

        Attributes:
            call_graph: The CallGraph object form which to extract the metrics.
    """

    def __init__(self, call_graph):
        """Constructor for BaseFormatter"""
        self.call_graph = call_graph

    @staticmethod
    def _get_template(template_file):
        template_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), template_file
        )

        if not settings.configured:
            settings.configure()

        template = None
        with open(template_file, 'r') as file_:
            template = file_.read()
        return Template(template)

    @staticmethod
    def _get_signature(call):
        return '' if not call.function_signature else call.function_signature

    @staticmethod
    def _transform_calls(calls):
        calls = [
            {
                'function_name': c.function_name,
                'function_signature': BaseFormatter._get_signature(c)
            } for c in calls
        ]
        return calls

    def write_summary(self):
        template = BaseFormatter._get_template(self.summary_template_file)

        context = Context({
            'directory': self.call_graph.source,
            'nodes_count': len(self.call_graph.nodes),
            'edges_count': len(self.call_graph.edges),
            'entry_points_count': len(self.call_graph.entry_points),
            'exit_points_count': len(self.call_graph.exit_points),
            'dangerous_functions_count':
                len(nx.get_node_attributes(
                    self.call_graph.call_graph, 'dangerous'
                )),
        })

        return template.render(context)

    def write_output(self):
        template = BaseFormatter._get_template(self.template_file)

        context = Context({
            'directory': self.call_graph.source,
            'nodes_count': len(self.call_graph.nodes),
            'nodes': [
                {
                    'function_name': c.function_name,
                    'function_signature': BaseFormatter._get_signature(c),
                    'degree': self.call_graph.get_degree(c)
                } for (c, attrs) in self.call_graph.nodes
            ],
            'edges_count': len(self.call_graph.edges),
            'edges': [
                {'from': f.function_name, 'to': t.function_name}
                for (f, t, attrs) in self.call_graph.edges
            ],
            'entry_points_count': len(self.call_graph.entry_points),
            'entry_points': BaseFormatter._transform_calls(
                self.call_graph.entry_points
            ),
            'exit_points_count': len(self.call_graph.exit_points),
            'exit_points': BaseFormatter._transform_calls(
                self.call_graph.exit_points
            ),
            'dangerous_functions_count':
                len(nx.get_node_attributes(
                    self.call_graph.call_graph, 'dangerous'
                )),
            'dangerous_functions':
                nx.get_node_attributes(
                    self.call_graph.call_graph, 'dangerous'
                ).keys(),
        })

        return template.render(context)

    @property
    def template_file(self):
        pass

    @property
    def summary_template_file(self):
        pass
