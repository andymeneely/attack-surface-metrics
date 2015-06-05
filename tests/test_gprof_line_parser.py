__author__ = 'kevin'

import unittest
from attacksurfacemeter.loaders.gprof_line_parser import GprofLineParser


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

    def test_spontaneous(self):
        # Assert
        self.assertRaises(ValueError, GprofLineParser.get_instance, 
            "                                                 <spontaneous>")

    def test_get_function_signature_with_path(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "[12]     0.0    0.00    0.00   72000         hScale_MMX "
            "(./libswscale/x86/swscale_template.c:1921 @ 9f46e0) [12]"
        )

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("./libswscale/x86/swscale_template.c", test_function_signature)

        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "                0.00    0.00    2590/5180        opt_find "
            "(./libavcodec/options.c:53 @ 77e710) [316705]"
        )

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("./libavcodec/options.c", test_function_signature)

        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "[49220   0.0    0.00    0.00                 "
            "__do_global_ctors_aux [492203]"
        )

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("", test_function_signature)

    def test_get_function_signature_include_files(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "                0.00    0.00       1/34841       snprintf "
            "(/usr/include/x86_64-linux-gnu/bits/stdio2.h:64 @ 47d37b) "
            "[650457]"
        )

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("/usr/include/x86_64-linux-gnu/bits/stdio2.h", 
            test_function_signature)

        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "                0.00    0.00       1/589         atoi "
            "(/usr/include/stdlib.h:280 @ 57c1fc) [26713]"
        )

        # Act
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("/usr/include/stdlib.h", test_function_signature)

    def test_load_recursive_call_line(self):
        # Arrange
        test_line_parser = GprofLineParser.get_instance(
            "[86901   0.0    0.00    0.00      12+12      _init [869011]"
        )

        # Act
        test_function_name = test_line_parser.get_function_name()
        test_function_signature = test_line_parser.get_function_signature()

        # Assert
        self.assertEqual("_init", test_function_name)
        self.assertEqual("", test_function_signature)

if __name__ == '__main__':
    unittest.main()
