__author__ = 'kevin'

import os

from django.template import Template, Context
from django.conf import settings

from formatters.base_formatter import BaseFormatter

from formatters.xml_formatter import XElement


class HtmlFormatter(BaseFormatter):

    def __init__(self, call_graph):
        super(HtmlFormatter, self).__init__(call_graph)

    def _get_template(self):
        template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template.html")
        settings.configure()

        return Template(open(template_file, 'r').read())

    def _get_function_signature(self, call):
        return '' if call.function_signature is None else call.function_signature

    def write_output(self):
        template = self._get_template()
        context = Context({
            'directory': self.source_dir,
            'nodes_count': self.nodes_count,
            'nodes': [{
                          'function_name': c.function_name,
                          'function_signature': '' if c.function_signature is None else c.function_signature,
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
                          'descendant_entry_points': [{'function_name': denp.function_name,
                                                       'function_signature': self._get_function_signature(denp)
                                                      } for denp in self.get_descendant_entry_points(c)],

                          'descendant_exit_points_count': self.get_descendant_exit_points_count(c),
                          'descendant_exit_points': [{'function_name': dexp.function_name,
                                                      'function_signature': self._get_function_signature(dexp)
                                                     } for dexp in self.get_descendant_exit_points(c)],

                          'ancestor_entry_points_count': self.get_ancestor_entry_points_count(c),
                          'ancestor_entry_points': [{'function_name': aenp.function_name,
                                                     'function_signature': self._get_function_signature(aenp)
                                                    } for aenp in self.get_ancestor_entry_points(c)],

                          'ancestor_exit_points_count': self.get_ancestor_exit_points_count(c),
                          'ancestor_exit_points': [{'function_name': aexp.function_name,
                                                    'function_signature': self._get_function_signature(aexp)
                                                   } for aexp in self.get_ancestor_exit_points(c)]
                      } for c in self.nodes]
        })




        # root = XElement("attack_surface",
        #                 {'directory': self.source_dir},
        #                 XElement("nodes",
        #                          {'count': self.nodes_count},
        #                          [self.call_to_xml(c,
        #                                            {
        #                                                'closeness': self.get_closeness(c),
        #                                                'betweenness': self.get_betweenness(c),
        #                                                'degree_centrality': self.get_degree_centrality(c),
        #                                                'in_degree_centrality': self.get_in_degree_centrality(c),
        #                                                'out_degree_centrality': self.get_out_degree_centrality(c),
        #                                                'degree': self.get_degree(c),
        #                                                'in_degree': self.get_in_degree(c),
        #                                                'out_degree': self.get_out_degree(c),
        #                                                'descendant_entry_points_ratio': self.get_descendants_entry_point_ratio(c),
        #                                                'descendant_exit_points_ratio': self.get_descendants_exit_point_ratio(c),
        #                                                'ancestor_entry_points_ratio': self.get_ancestors_entry_point_ratio(c),
        #                                                'ancestor_exit_points_ratio': self.get_ancestors_exit_point_ratio(c)
        #                                            },
        #                                            XElement('descendant_entry_points',
        #                                                     {'count': self.get_descendant_entry_points_count(c)},
        #                                                     [self.call_to_xml(c) for c in self.get_descendant_entry_points(c)]),
        #                                            XElement('descendant_exit_points',
        #                                                     {'count': self.get_descendant_exit_points_count(c)},
        #                                                     [self.call_to_xml(c) for c in self.get_descendant_exit_points(c)]),
        #                                            XElement('ancestor_entry_points',
        #                                                     {'count': self.get_ancestor_entry_points_count(c)},
        #                                                     [self.call_to_xml(c) for c in self.get_ancestor_entry_points(c)]),
        #                                            XElement('ancestor_exit_points',
        #                                                     {'count': self.get_ancestor_exit_points_count(c)},
        #                                                     [self.call_to_xml(c) for c in self.get_ancestor_exit_points(c)]))
        #                           for c in self.nodes]),
        #
        #                 XElement("edges",
        #                          {'count': self.edges_count},
        #                          [XElement('edge',
        #                                    {'from': f.function_name, 'to': t.function_name})
        #                           for (f, t) in self.edges]),
        #
        #                 XElement('entry_points',
        #                          {'count': self.entry_points_count},
        #                          [self.call_to_xml(c) for c in self.entry_points]),
        #
        #                 XElement('exit_points',
        #                          {'count': self.exit_points_count},
        #                          [self.call_to_xml(c) for c in self.exit_points]),
        #
        #                 XElement('execution_paths',
        #                          {
        #                              'count': self.execution_paths_count,
        #                              'average': self.average_execution_path_length,
        #                              'median': self.median_execution_path_length
        #                          },
        #                          [XElement('path', {'length': str(len(xp))}, xp)
        #                           for xp in [[self.call_to_xml(c) for c in p]
        #                                      for p in self.execution_paths]]),
        #
        #                 XElement('clustering',
        #                          {'entry_points_clustering': self.entry_points_clustering,
        #                           'exit_points_clustering': self.exit_points_clustering})
        # )

        output = template.render(context)

        print(output)
