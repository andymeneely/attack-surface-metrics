__author__ = 'kevin'

import unittest
from loaders.javacg_line_parser import JavaCGLineParser


class JavaCGLineParserTestCase(unittest.TestCase):

    def test_get_function_name_caller(self):
        # Arrange
        test_line_parser = JavaCGLineParser.get_instance("M:com.example.kevin.helloandroid.Greeter:sayHello")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("sayHello", test_function_name)

    def test_get_function_signature_caller(self):
        # Arrange
        test_line_parser = JavaCGLineParser.get_instance("M:com.example.kevin.helloandroid.Greeter:sayHello")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("com.example.kevin.helloandroid.Greeter", test_function_signature)

    def test_get_function_name_callee(self):
        # Arrange
        test_line_parser = JavaCGLineParser.get_instance("(M)java.lang.StringBuilder:append")

        # Act
        test_function_name = test_line_parser.get_function_name()

        # Assert
        self.assertEqual("append", test_function_name)

    def test_get_function_signature_callee(self):
        # Arrange
        test_line_parser = JavaCGLineParser.get_instance("(M)java.lang.StringBuilder:append")

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("java.lang.StringBuilder", test_function_signature)


if __name__ == '__main__':
    unittest.main()