__author__ = 'kevin'

import unittest
from attacksurfacemeter import CflowCall


class CallTestCase(unittest.TestCase):

    def test_identity_function_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertEqual("printf", test_call.identity)

    def test_identity_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertEqual("xstrdup xmalloc.c", test_call.identity)

    def test_function_name_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertEqual("printf", test_call.function_name)

    def test_function_name_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertEqual("xstrdup", test_call.function_name)

    def test_function_signature_only_name(self):
        # Arrange
        cflow_line = "printf()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertIsNone(test_call.function_signature)

    def test_function_signature_full(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = CflowCall(cflow_line)

        # Assert
        # self.assertEqual("<char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89>", test_call.function_signature)
        self.assertEqual("xmalloc.c", test_call.function_signature)

    def test_is_input_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertTrue(test_call.is_input_function())

    def test_is_not_input_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_not_input_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input_function())

    def test_is_output_function(self):
        # Arrange
        cflow_line = "printf()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertTrue(test_call.is_output_function())

    def test_is_not_output_function(self):
        # Arrange
        cflow_line = "getchar()"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_is_not_output_function_no_leaf(self):
        # Arrange
        cflow_line = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call = CflowCall(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output_function())

    def test_equal(self):
        # Arrange
        cflow_line = "getchar()"
        test_call_1 = CflowCall(cflow_line)
        test_call_2 = CflowCall(cflow_line)

        # Assert
        self.assertEqual(test_call_1, test_call_2)

    def test_not_equal(self):
        # Arrange
        cflow_line_1 = "getchar()"
        cflow_line_2 = "xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc.c:89> (R):"
        test_call_1 = CflowCall(cflow_line_1)
        test_call_2 = CflowCall(cflow_line_2)

        # Assert
        self.assertNotEqual(test_call_1, test_call_2)

if __name__ == '__main__':
    unittest.main()