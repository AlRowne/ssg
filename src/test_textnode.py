import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
