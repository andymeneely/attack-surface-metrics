import unittest

from attacksurfacemeter.loaders.base_loader import BaseLoader

class BaseLoaderTestCase(unittest.TestCase):
    def test_init_defaults(self):
        # Arrange
        source = '/tmp'

        # Act
        target = BaseLoader(source)

        # Assert
        self.assertEqual(source, target.source)
        self.assertFalse(target.is_reverse)
        self.assertIsNotNone(target.defenses)
        self.assertIsInstance(target.defenses, list)
        self.assertIsNotNone(target.vulnerabilities)
        self.assertIsInstance(target.vulnerabilities, list)
        self.assertCountEqual(list(), target.errors)

    def test_init(self):
        # Arrange
        source = '/tmp'
        is_reverse = True
        defenses = ['foo', 'bar']
        vulnerabilities = ['bar', 'baz']

        # Act
        target = BaseLoader(source, is_reverse, defenses, vulnerabilities)

        # Assert
        self.assertEqual(source, target.source)
        self.assertTrue(target.is_reverse)
        self.assertIsNotNone(target.defenses)
        self.assertCountEqual(defenses, target.defenses)
        self.assertIsNotNone(target.vulnerabilities)
        self.assertCountEqual(vulnerabilities, target.vulnerabilities)
        self.assertCountEqual(list(), target.errors)

    def test_load_call_graph(self):
        # Arrange
        source = '/tmp'

        # Act
        target = BaseLoader(source)

        # Assert
        self.assertRaises(NotImplementedError, target.load_call_graph)

if __name__ == '__main__':
    unittest.main()
