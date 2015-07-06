import os

from attacksurfacemeter.call import Call
from attacksurfacemeter.call_graph import CallGraph
from attacksurfacemeter.loaders.cflow_loader import CflowLoader
from attacksurfacemeter.formatters.txt_formatter import TxtFormatter


class BaseFormatterTests(object):
    def test_write_output(self):
        # Arrange
        expected = None
        with open(self.formatter_output_file) as file_:
            expected = file_.readlines()

        # Act
        actual = self.formatter.write_output().splitlines(keepends=True)

        with open('output.xml', 'w') as file_:
            file_.write(self.formatter.write_output())

        # Assert
        self.assertEqual(len(expected), len(actual))

    def test_write_summary(self):
        # Arrange
        expected = None
        with open(self.formatter_summary_file) as file_:
            expected = file_.readlines()

        # Act
        actual = self.formatter.write_summary().splitlines(keepends=True)

        with open('summary.xml', 'w') as file_:
            file_.write(self.formatter.write_summary())

        # Assert
        self.assertEqual(len(expected), len(actual))


if __name__ == '__main__':
    unittest.main()
