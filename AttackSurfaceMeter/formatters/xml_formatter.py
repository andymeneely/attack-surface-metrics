__author__ = 'kevin'

import xml.etree.ElementTree as Xml
from xml.dom.minidom import parseString

from formatters.base_formatter import BaseFormatter


class XmlFormatter(BaseFormatter):
    def __init__(self, call_graph):
        super(XmlFormatter, self).__init__(call_graph)

    def write_output(self):
        root = XElement("attacksurface",
                        {'directory': self.call_graph.source_dir},
                        XElement("nodes",
                                 {'count': str(len(self.call_graph.nodes))},
                                 [XElement(c.function_name) for c in self.call_graph.nodes]),
                        XElement("whatever"))

        print(self.prettyfy(root))

    def prettyfy(self, xml_element):
        return parseString(
            Xml.tostring(xml_element, encoding="unicode")
        ).toprettyxml()


class XElement(Xml.Element):
    def __init__(self, tag, atrributes={}, *subelements):

        super(XElement, self).__init__(tag, atrributes)

        for subelement in subelements:
            if isinstance(subelement, list):
                self.extend(subelement)
            else:
                self.append(subelement)