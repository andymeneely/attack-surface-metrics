__author__ = 'kevin'

import unittest
from formatters.xml_formatter import XElement


class XElementTestCase(unittest.TestCase):

    def test_constructor(self):
        # Arrange
        tag = "element"

        # Act
        xelem = XElement(tag)

        # Assert
        self.assertEqual(tag, xelem.tag)

    def test_constructor_with_attributes(self):
        # Arrange
        expected_attribs = {'att0': 0, 'att1': 1}

        # Act
        xelem = XElement('element', expected_attribs)

        # Assert
        self.assertEqual(expected_attribs, xelem.attrib)

    def test_constructor_with_subelements_as_list(self):
        # Arrange
        expected_subelements = [XElement('subelem0'), XElement('subelem1')]

        # Act
        xelem = XElement('element',
                         {'att0': 0, 'att1': 1},
                         expected_subelements)

        all_subelements_found = all([x in list(xelem) for x in expected_subelements])

        # Assert
        self.assertTrue(all_subelements_found)

    def test_constructor_with_subelements_as_positional_arguments(self):
        # Arrange
        expected_subelement_1 = XElement('subelem0')
        expected_subelement_2 = XElement('subelem1')

        # Act
        xelem = XElement('element',
                         {'att0': 0, 'att1': 1},
                         expected_subelement_1,
                         expected_subelement_2)

        all_subelements_found = all([expected_subelement_1 in list(xelem),
                                     expected_subelement_2 in list(xelem)])

        # Assert
        self.assertTrue(all_subelements_found)

if __name__ == '__main__':
    unittest.main()