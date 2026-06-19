import unittest

from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_bold(self):
        node = TextNode("hello **world** end", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** and plain", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and plain", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("plain and **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("plain and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_only_delimiter_content(self):
        node = TextNode("**bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])

    def test_multiple_delimiter_pairs(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.BOLD),
                TextNode(" e", TextType.TEXT),
            ],
        )

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
        self.assertEqual(
            result,
            [
                TextNode("already italic", TextType.ITALIC),
                TextNode("say ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_multiple_text_nodes_all_processed(self):
        nodes = [
            TextNode("**a**", TextType.TEXT),
            TextNode("**b**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.BOLD),
            ],
        )

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
        self.assertEqual(
            result,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def test_code_delimiter(self):
        node = TextNode("run `ls -la` now", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("run ", TextType.TEXT),
                TextNode("ls -la", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_adjacent_delimiter_pairs(self):
        node = TextNode("**a****b**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.BOLD),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "text before ![alt](https://i.img/a.png) text after", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://i.img/a.png"),
                TextNode(" text after", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "![one](https://i.img/1.png) mid ![two](https://i.img/2.png) end",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("one", TextType.IMAGE, "https://i.img/1.png"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://i.img/2.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_image_only(self):
        node = TextNode("![alt](https://i.img/a.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [TextNode("alt", TextType.IMAGE, "https://i.img/a.png")],
        )

    def test_adjacent_images_no_text_between(self):
        node = TextNode(
            "![a](https://i.img/a.png)![b](https://i.img/b.png)", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "https://i.img/a.png"),
                TextNode("b", TextType.IMAGE, "https://i.img/b.png"),
            ],
        )

    def test_no_image_passthrough(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("plain text only", TextType.TEXT)])

    def test_non_text_node_passthrough(self):
        node = TextNode("alt", TextType.IMAGE, "https://i.img/a.png")
        result = split_nodes_image([node])
        self.assertEqual(
            result, [TextNode("alt", TextType.IMAGE, "https://i.img/a.png")]
        )

    def test_link_is_not_treated_as_image(self):
        node = TextNode("a [link](https://boot.dev) here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(
            result, [TextNode("a [link](https://boot.dev) here", TextType.TEXT)]
        )

    def test_empty_input(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_mixed_node_list(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("see ![pic](https://i.img/p.png)!", TextType.TEXT),
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("see ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://i.img/p.png"),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_duplicate_images(self):
        node = TextNode(
            "![a](https://i.img/a.png) and ![a](https://i.img/a.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "https://i.img/a.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://i.img/a.png"),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "text before [to boot](https://boot.dev) text after", TextType.TEXT
        )
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("to boot", TextType.LINK, "https://boot.dev"),
                TextNode(" text after", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "[one](https://a.dev) mid [two](https://b.dev) end", TextType.TEXT
        )
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("one", TextType.LINK, "https://a.dev"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://b.dev"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_link_only(self):
        node = TextNode("[to boot](https://boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [TextNode("to boot", TextType.LINK, "https://boot.dev")],
        )

    def test_no_link_passthrough(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("plain text only", TextType.TEXT)])

    def test_non_text_node_passthrough(self):
        node = TextNode("to boot", TextType.LINK, "https://boot.dev")
        result = split_nodes_link([node])
        self.assertEqual(
            result, [TextNode("to boot", TextType.LINK, "https://boot.dev")]
        )

    def test_image_is_not_treated_as_link(self):
        node = TextNode("an ![pic](https://i.img/p.png) here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [TextNode("an ![pic](https://i.img/p.png) here", TextType.TEXT)],
        )

    def test_link_alongside_image_only_link_split(self):
        node = TextNode(
            "![pic](https://i.img/p.png) and [link](https://boot.dev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("![pic](https://i.img/p.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_empty_input(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_mixed_node_list(self):
        nodes = [
            TextNode("already code", TextType.CODE),
            TextNode("go [here](https://boot.dev)!", TextType.TEXT),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("already code", TextType.CODE),
                TextNode("go ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://boot.dev"),
                TextNode("!", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
