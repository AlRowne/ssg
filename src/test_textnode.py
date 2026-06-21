import unittest

from textnode import TextNode, TextType
from textnode_to_html import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        node2 = TextNode("click here", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("click", TextType.LINK, "https://a.com")
        node2 = TextNode("click", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_non_textnode(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(node, "hello")

    def test_url_default_none(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_set(self):
        node = TextNode("img", TextType.IMAGE, "https://img.com/pic.png")
        self.assertEqual(node.url, "https://img.com/pic.png")

    def test_text_attribute(self):
        node = TextNode("hello", TextType.CODE)
        self.assertEqual(node.text, "hello")

    def test_text_type_attribute(self):
        node = TextNode("hello", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_repr(self):
        node = TextNode("hello", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(hello, bold, None)")

    def test_repr_with_url(self):
        node = TextNode("click", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node), "TextNode(click, link, https://example.com)")

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        node2 = TextNode("", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")

    def test_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")

    def test_code(self):
        node = TextNode("code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code")

    def test_link(self):
        node = TextNode("click", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_link_requires_url(self):
        node = TextNode("click", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://img.com/pic.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://img.com/pic.png", "alt": "alt text"},
        )

    def test_image_requires_url(self):
        node = TextNode("alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
