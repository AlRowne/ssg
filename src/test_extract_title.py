import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_expected(self):
        md = "# Title"
        result = extract_title(md)

        self.assertEqual(result, "Title")

    def test_leading_whitespace(self):
        md = "   # Title"
        result = extract_title(md)

        self.assertEqual(result, "Title")

    def test_leading_and_trailing_whitespace(self):
        md = "     # Title    "
        result = extract_title(md)

        self.assertEqual(result, "Title")

    def test_raise(self):
        md = "> Quote"
        with self.assertRaises(ValueError):
            extract_title(md)
