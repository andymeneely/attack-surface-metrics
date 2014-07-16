__author__ = 'kevin'

import xml.etree.ElementTree as Xml
from xml.dom.minidom import parseString

from formatters.base_formatter import BaseFormatter

# TODO: Refactor out of this class and into BaseFormatter all the
# code that accesses call_graph properties and functions.
# Ideally, derived formatter classes will send lambdas to
# their base class's methods that will serve as selectors
# for the various collections.


class XmlFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(XmlFormatter, self).__init__(call_graph)

    def write_output(self):
        root = XElement("attack_surface",
                        {'directory': self.source_dir},
                        XElement("nodes",
                                 {'count': self.nodes_count},
                                 [self.call_to_xml(c,
                                                   {
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
                                                       'ancestor_exit_points_ratio': self.get_ancestors_exit_point_ratio(c)
                                                   },
                                                   XElement('descendant_entry_points',
                                                            {'count': self.get_count_descendant_entry_points(c)},
                                                            [self.call_to_xml(c) for c in self.get_descendant_entry_points(c)]),
                                                   XElement('descendant_exit_points',
                                                            {'count': self.get_count_descendant_exit_points(c)},
                                                            [self.call_to_xml(c) for c in self.get_descendant_exit_points(c)]),
                                                   XElement('ancestor_entry_points',
                                                            {'count': self.get_count_ancestor_entry_points(c)},
                                                            [self.call_to_xml(c) for c in self.get_ancestor_entry_points(c)]),
                                                   XElement('ancestor_exit_points',
                                                            {'count': self.get_count_ancestor_exit_points(c)},
                                                            [self.call_to_xml(c) for c in self.get_ancestor_exit_points(c)]))
                                  for c in self.nodes]),

                        XElement("edges",
                                 {'count': self.edges_count},
                                 [XElement('edge',
                                           {'from': f.function_name, 'to': t.function_name})
                                  for (f, t) in self.edges]),

                        XElement('entry_points',
                                 {'count': self.entry_points_count},
                                 [self.call_to_xml(c) for c in self.entry_points]),

                        XElement('exit_points',
                                 {'count': self.exit_points_count},
                                 [self.call_to_xml(c) for c in self.exit_points]),

                        XElement('execution_paths',
                                 {'count': self.execution_paths_count,
                                  'average': self.average_execution_path_length,
                                  'median': self.median_execution_path_length},
                                 [XElement('path', {'length': str(len(xp))}, xp)
                                  for xp in [[self.call_to_xml(c) for c in p]
                                             for p in self.execution_paths]]),

                        XElement('clustering',
                                 {'entry_points_clustering': self.entry_points_clustering,
                                  'exit_points_clustering': self.exit_points_clustering})
        )

        print(self.prettyfy(root))

    def prettyfy(self, xml_element):
        """

            Args:
                :

            Returns:


            Raises:
                :
        """
        return parseString(
            Xml.tostring(xml_element, encoding="unicode")
        ).toprettyxml()

    def call_to_xml(self, call, attributes={}, *subelements):
        attributes.update({'name': call.function_name,
                           'signature': '' if call.function_signature is None else call.function_signature})
        elem = XElement('call', attributes, list(subelements))

        return elem


class XElement(Xml.Element):
    def __init__(self, tag, atrributes={}, *subelements):

        super(XElement, self).__init__(tag, atrributes)

        for subelement in subelements:
            if isinstance(subelement, list):
                self.extend(subelement)
            else:
                self.append(subelement)