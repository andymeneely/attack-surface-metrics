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
                        {'directory': self.call_graph.source_dir},
                        XElement("nodes",
                                 {'count': str(len(self.call_graph.nodes))},
                                 [XElement('call',
                                           {
                                               'function_name': c.function_name,
                                               'closeness': str(self.call_graph.get_closeness(c)),
                                               'betweenness': str(self.call_graph.get_betweenness(c)),
                                               'degree_centrality': str(self.call_graph.get_degree_centrality(c)),
                                               'in_degree_centrality': str(self.call_graph.get_in_degree_centrality(c)),
                                               'out_degree_centrality': str(self.call_graph.get_out_degree_centrality(c)),
                                               'degree': str(self.call_graph.get_degree(c)),
                                               'in_degree': str(self.call_graph.get_in_degree(c)),
                                               'out_degree': str(self.call_graph.get_out_degree(c)),
                                               'descendant_entry_points_ratio': str(self.call_graph.get_descendants_exit_point_ratio(c)),
                                               'descendant_exit_points_ratio': str(self.call_graph.get_ancestors_entry_point_ratio(c)),
                                               'ancestor_entry_points_ratio': str(self.call_graph.get_ancestors_exit_point_ratio(c)),
                                               'ancestor_exit_points_ratio': str(self.call_graph.get_ancestors_entry_point_ratio(c))
                                           },
                                           XElement('descendant_entry_points',
                                                    {'count': str(len(self.call_graph.get_descendant_entry_points(c)))},
                                                    [self.call_to_xml(c) for c in self.call_graph.get_descendant_entry_points(c)]),
                                           XElement('descendant_exit_points',
                                                    {'count': str(len(self.call_graph.get_descendant_exit_points(c)))},
                                                    [self.call_to_xml(c) for c in self.call_graph.get_descendant_exit_points(c)]),
                                           XElement('ancestor_entry_points',
                                                    {'count': str(len(self.call_graph.get_ancestor_entry_points(c)))},
                                                    [self.call_to_xml(c) for c in self.call_graph.get_ancestor_entry_points(c)]),
                                           XElement('ancestor_exit_points',
                                                    {'count': str(len(self.call_graph.get_ancestor_exit_points(c)))},
                                                    [self.call_to_xml(c) for c in self.call_graph.get_ancestor_exit_points(c)]))
                                  for c in self.call_graph.nodes]),

                        XElement("edges",
                                 {'count': str(len(self.call_graph.edges))},
                                 [XElement('edge',
                                           {'from': f.function_name, 'to': t.function_name})
                                  for (f, t) in self.call_graph.edges]),

                        XElement('entry_points',
                                 {'count': str(len(self.call_graph.entry_points))},
                                 [self.call_to_xml(c) for c in self.call_graph.entry_points]),

                        XElement('exit_points',
                                 {'count': str(len(self.call_graph.exit_points))},
                                 [self.call_to_xml(c) for c in self.call_graph.exit_points]),

                        XElement('execution_paths',
                                 {'count': str(len(self.call_graph.execution_paths))},
                                 [XElement('path', {'length': str(len(xp))}, xp)
                                  for xp in [[self.call_to_xml(c) for c in p]
                                             for p in self.call_graph.execution_paths]]),

                        XElement('clustering',
                                 {'avg_entry_point_clustering': str(self.call_graph.entry_points_clustering),
                                  'avg_exit_point_clustering': str(self.call_graph.exit_points_clustering)})
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

    def call_to_xml(self, call, **extras):
        elem = XElement('call', {'function_name': call.function_name})
        elem.attrib.update(extras)

        return elem


class XElement(Xml.Element):
    def __init__(self, tag, atrributes={}, *subelements):

        super(XElement, self).__init__(tag, atrributes)

        for subelement in subelements:
            if isinstance(subelement, list):
                self.extend(subelement)
            else:
                self.append(subelement)