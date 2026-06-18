import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_bold(self):
        node = TextNode("hello **world** end", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" end", TextType.TEXT),
        ])

    def test_delimiter_at_start(self):
        node = TextNode("**bold** and plain", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and plain", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("plain and **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("plain and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_only_delimiter_content(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_multiple_delimiter_pairs(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ])

    def test_no_delimiter_in_text(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("plain text", TextType.TEXT)])

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_node_list(self):
        nodes = [
            TextNode("already italic", TextType.ITALIC),
            TextNode("say `code` here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("already italic", TextType.ITALIC),
            TextNode("say ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_multiple_text_nodes_all_processed(self):
        nodes = [
            TextNode("**a**", TextType.TEXT),
            TextNode("**b**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("a", TextType.BOLD),
            TextNode("b", TextType.BOLD),
        ])

    def test_empty_input(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("open **unclosed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_italic_delimiter(self):
        node = TextNode("hello *italic* world", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", TextType.TEXT),
        ])

    def test_code_delimiter(self):
        node = TextNode("run `ls -la` now", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("run ", TextType.TEXT),
            TextNode("ls -la", TextType.CODE),
            TextNode(" now", TextType.TEXT),
        ])

    def test_adjacent_delimiter_pairs(self):
        node = TextNode("**a****b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("a", TextType.BOLD),
            TextNode("b", TextType.BOLD),
        ])


if __name__ == "__main__":
    unittest.main()
