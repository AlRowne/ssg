import unittest

from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_blocktype_heading(self):
        text = "### This is a heading"
        result = block_to_block_type(text)

        self.assertEqual(result, BlockType.HEADING)

    def test_blocktype_heading_all_levels(self):
        for hashes in ["#", "##", "###", "####", "#####", "######"]:
            text = f"{hashes} heading"
            self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_blocktype_heading_seven_hashes_is_paragraph(self):
        text = "####### too many hashes"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_heading_no_space_is_paragraph(self):
        text = "###nospace"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        text = "```\nsome code\nmore code\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_blocktype_quote(self):
        text = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_blocktype_quote_mixed_is_paragraph(self):
        text = "> line one\nline two without quote"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_unordered_list(self):
        text = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_list_mixed_is_paragraph(self):
        text = "- item one\nitem two without dash"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list(self):
        text = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_blocktype_ordered_list_gap_is_paragraph(self):
        text = "1. first\n3. third"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list_not_starting_at_one_is_paragraph(self):
        text = "2. second\n3. third"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_blocktype_paragraph(self):
        text = "Just a normal paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)
