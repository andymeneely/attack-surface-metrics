__author__ = 'kevin'

import unittest
from loaders.gprof_line_parser import GprofLineParser


class GprofLineParserTestCase(unittest.TestCase):

    def test_get_function_name_entry(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("[4]      0.0    0.00    0.00       2         greet (greetings.c:38 @ 581033) [4]")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("greet", test_function_name)

    def test_get_function_signature_entry(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("[4]      0.0    0.00    0.00       2         greet (greetings.c:38 @ 581033) [4]")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("greetings.c", test_function_signature)

    def test_get_function_name_with_self_and_children(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("                0.00    0.00       1/2           greet_b (helloworld.c:38 @ 581033) [9]")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("greet_b", test_function_name)

    def test_get_function_signature_with_self_and_children(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("                0.00    0.00       1/2           greet_b (helloworld.c:38 @ 581033) [9]")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("helloworld.c", test_function_signature)

    def test_get_function_name_with_called_only(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("                                   8             recursive_a <cycle 1> (greetings.c:38 @ 581033) [3]")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("recursive_a", test_function_name)

    def test_get_function_signature_with_called_only(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance("                                   8             recursive_a <cycle 1> (greetings.c:38 @ 581033) [3]")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("greetings.c", test_function_signature)


if __name__ == '__main__':
    unittest.main()