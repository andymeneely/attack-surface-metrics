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
                                 [self.call_to_xml(c) for c in self.call_graph.nodes]),

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

                        XElement('closeness', {},
                                 [self.call_to_xml(k, closeness=str(v))
                                  for k, v in self.call_graph.get_closeness().items()]),

                        XElement('betweenness', {},
                                 [self.call_to_xml(k, betweenness=str(v))
                                  for k, v in self.call_graph.get_betweenness().items()]),
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