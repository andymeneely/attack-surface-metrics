__author__ = 'kevin'

import xml.etree.ElementTree as Xml
from xml.dom.minidom import parseString

from attacksurfacemeter.formatters.base_formatter import BaseFormatter


class XmlFormatter(BaseFormatter):
    """
        Produces an xml report with the attack surface metrics calculated by call_graph
        and prints it to console.
    """
    def __init__(self, call_graph):
        super(XmlFormatter, self).__init__(call_graph)

    def write_summary(self):
        root = XElement("attack_surface",
                        {'directory': self.source},

                        XElement("nodes", {'count': self.nodes_count}),
                        XElement("edges", {'count': self.edges_count}),
                        XElement('entry_points', {'count': self.entry_points_count}),
                        XElement('exit_points', {'count': self.exit_points_count}),
                        XElement('execution_paths',
                                 {
                                     'count': self.execution_paths_count,
                                     'average': self.average_execution_path_length,
                                     'median': self.median_execution_path_length
                                 }),
                        XElement('closeness',
                                 {
                                     'average': self.average_closeness,
                                     'median': self.median_closeness
                                 }),
                        XElement('betweenness',
                                 {
                                     'average': self.average_betweenness,
                                     'median': self.median_betweenness
                                 }),
                        XElement('clustering',
                                 {
                                     'entry_points_clustering': self.entry_points_clustering,
                                     'exit_points_clustering': self.exit_points_clustering
                                 }),
                        XElement('centrality',
                                 {
                                     'average_degree_centrality': self.average_degree_centrality,
                                     'median_degree_centrality': self.median_degree_centrality,
                                     'average_in_degree_centrality': self.average_in_degree_centrality,
                                     'median_in_degree_centrality': self.median_in_degree_centrality,
                                     'average_out_degree_centrality': self.average_out_degree_centrality,
                                     'median_out_degree_centrality': self.median_out_degree_centrality
                                 }),
                        XElement('degree',
                                 {
                                     'average_degree': self.average_degree,
                                     'median_degree': self.median_degree,
                                     'average_in_degree': self.average_in_degree,
                                     'median_in_degree': self.median_in_degree,
                                     'average_out_degree': self.average_out_degree,
                                     'median_out_degree': self.median_out_degree
                                 }))

        return self.prettyfy(root)

    def write_output(self):
        root = XElement("attack_surface",
                        {'directory': self.source},
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
                                                            {'count': self.get_descendant_entry_points_count(c)},
                                                            [self.call_to_xml(c) for c in self.get_descendant_entry_points(c)]),
                                                   XElement('descendant_exit_points',
                                                            {'count': self.get_descendant_exit_points_count(c)},
                                                            [self.call_to_xml(c) for c in self.get_descendant_exit_points(c)]),
                                                   XElement('ancestor_entry_points',
                                                            {'count': self.get_ancestor_entry_points_count(c)},
                                                            [self.call_to_xml(c) for c in self.get_ancestor_entry_points(c)]),
                                                   XElement('ancestor_exit_points',
                                                            {'count': self.get_ancestor_exit_points_count(c)},
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
                                 {
                                     'count': self.execution_paths_count,
                                     'average': self.average_execution_path_length,
                                     'median': self.median_execution_path_length
                                 },
                                 [XElement('path', {'length': str(len(xp))}, xp)
                                  for xp in [[self.call_to_xml(c) for c in p]
                                             for p in self.execution_paths]]),

                        XElement('clustering',
                                 {'entry_points_clustering': self.entry_points_clustering,
                                  'exit_points_clustering': self.exit_points_clustering})
        )

        return self.prettyfy(root)

    def prettyfy(self, xml_element):
        """
            Returns a pretty formatted string representation of a given xml element and its descendants.
        """
        return parseString(
            Xml.tostring(xml_element, encoding="unicode")
        ).toprettyxml()

    def call_to_xml(self, call, attributes={}, *subelements):
        """
            Creates an XElement object from a given Call object.

            Adds name and signature attributes to the created XElement.

            Args:
                call: An instance of Call to use to generate the XElement.
                attibutes: An optional dictionary containing additional attributes to include in
                    the created XElement.
                subelements: A list or series of positional XElement objects that will be added
                    as subelements to the created XElement.

            Returns:
                An instance of XElement based on the given Call object and the additional data provided.
        """
        attributes.update({'name': call.function_name,
                           'signature': '' if call.function_signature is None else call.function_signature})
        elem = XElement('call', attributes, list(subelements))

        return elem


class XElement(Xml.Element):
    """
        Wraps around xml.etree.ElementTree.Element to provide a more declarative way of constructing XML trees.
    """
    def __init__(self, tag, atrributes={}, *subelements):
        """
            Constructor for XElement.

            Provides de ability to send subelements as arguments to achieve a declarative way of creating XML trees.

            Args:
                tag: A string representing the tag of the XML element to create.
                attibutes: An optional dictionary containing additional attributes to include in
                    the created XElement.
                subelements: A list or series of positional XElement objects that will be added
                    as subelements to the created XElement.
        """
        super(XElement, self).__init__(tag, atrributes)

        for subelement in subelements:
            if isinstance(subelement, list):
                self.extend(subelement)
            else:
                self.append(subelement)
