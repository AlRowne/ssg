import unittest

from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_default_block(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """

        result = markdown_to_blocks(text)

        self.assertEqual(
            result,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        text = ""
        result = markdown_to_blocks(text)

        self.assertEqual(result, [])

    def test_multiplet_newlines(self):
        text = """This is a test


        with multiple





        newlines."""
        result = markdown_to_blocks(text)

        self.assertEqual(result, ["This is a test", "with multiple", "newlines."])
