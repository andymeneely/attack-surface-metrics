__author__ = 'kevin'

import unittest
from attacksurfacemeter.loaders.cflow_line_parser import CflowLineParser


class CflowLineParserTestCase(unittest.TestCase):

    def test_get_function_name(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("GreeterSayHi", test_function_name)

    def test_get_function_signature(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("./src/helloworld.c", test_function_signature)

    def test_get_function_name_name_only(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("            printf()")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("printf", test_function_name)

    def test_get_function_signature_name_only(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("            printf()")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("", test_function_signature)

    def test_get_level_0(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("GreeterSayHi() <void GreeterSayHi () at ./src/helloworld.c:48>:")

        # Act
        test_level = test_line_parser.get_level()

        # Assert
        self.assertEqual(0, test_level)

    def test_get_level_1(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("    recursive_a() <void recursive_a (int i) at ./src/greetings.c:26> (R):")

        # Act
        test_level = test_line_parser.get_level()

        # Assert
        self.assertEqual(1, test_level)

    def test_get_level_2(self):
        # Arrange
        test_line_parser = CflowLineParser.get_instance("        recursive_b() <void recursive_b (int i) at ./src/greetings.c:32> (R):")

        # Act
        test_level = test_line_parser.get_level()

        # Assert
        self.assertEqual(2, test_level)


if __name__ == '__main__':
    unittest.main()