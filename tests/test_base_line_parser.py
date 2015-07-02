import unittest

from attacksurfacemeter.loaders.base_line_parser import BaseLineParser

class BaseLineParserTestCase(unittest.TestCase):
    def setUp(self):
        self.target = BaseLineParser()

    def test_init_defaults(self):
        # Arrange
        expected = ''

        # Assert
        self.assertEqual(expected, self.target._function_name)
        self.assertEqual(expected, self.target._function_signature)

    def test_get_function_name(self):
        # Arrange
        expected = ''

        # Act
        actual = self.target.get_function_name()

        # Assert
        self.assertEqual(expected, actual)

    def test_get_function_signature(self):
        # Arrange
        expected = ''

        # Act
        actual = self.target.get_function_signature()

        # Assert
        self.assertEqual(expected, actual)

    def test_load(self):
        # Arrange
        line = '        main() <int main (void) at ./src/helloworld.c:58>'

        # Assert
        self.assertRaises(NotImplementedError, self.target.load, line)

    def test_load_if_new(self):
        # Arrange
        line = '        main() <int main (void) at ./src/helloworld.c:58>'

        # Assert
        self.assertRaises(NotImplementedError, self.target._load_if_new, line)

if __name__ == '__main__':
    unittest.main()
