import unittest

from attacksurfacemeter.call import Call
from attacksurfacemeter.granularity import Granularity


class CallTestCase(unittest.TestCase):
    def test_identity_function_name(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('printf', test_call.identity)

    def test_identity_function_name_file_granularity(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line, granularity=Granularity.FILE)

        # Assert
        self.assertEqual('', test_call.identity)

    def test_identity_full(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('xstrdup ./cyrus/lib/xmalloc.c', test_call.identity)

    def test_identity_full_file_granularity(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line, granularity=Granularity.FILE)

        # Assert
        self.assertEqual('./cyrus/lib/xmalloc.c', test_call.identity)

    def test_function_name_only_name(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('printf', test_call.function_name)

    def test_function_name_full(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('xstrdup', test_call.function_name)

    def test_function_signature_only_name(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('', test_call.function_signature)

    def test_function_signature_full(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual('./cyrus/lib/xmalloc.c', test_call.function_signature)

    def test_is_input(self):
        # Arrange
        cflow_line = 'getchar()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertTrue(test_call.is_input())

    def test_is_not_input(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input())

    def test_is_not_input_no_leaf(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertFalse(test_call.is_input())

    def test_is_output(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertTrue(test_call.is_output())

    def test_is_not_output(self):
        # Arrange
        cflow_line = 'getchar()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output())

    def test_is_not_output_no_leaf(self):
        # Arrange
        cflow_line = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertFalse(test_call.is_output())

    def test_equal(self):
        # Arrange
        cflow_line = 'getchar()'
        test_call_1 = Call.from_cflow(cflow_line)
        test_call_2 = Call.from_cflow(cflow_line)

        # Assert
        self.assertEqual(test_call_1, test_call_2)

    def test_not_equal(self):
        # Arrange
        cflow_line_1 = 'getchar()'
        cflow_line_2 = (
            'xstrdup() <char *xstrdup (const char *str) at ./cyrus/lib/xmalloc'
            '.c:89> (R):'
        )
        test_call_1 = Call.from_cflow(cflow_line_1)
        test_call_2 = Call.from_cflow(cflow_line_2)

        # Assert
        self.assertNotEqual(test_call_1, test_call_2)

    def test_in_stdlib(self):
        # Arrange
        cflow_line = 'printf()'
        test_call = Call.from_cflow(cflow_line)

        # Assert
        self.assertTrue(test_call.in_stdlib())


if __name__ == '__main__':
    unittest.main()
