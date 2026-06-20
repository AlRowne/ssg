import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_simple(self):
        node = LeafNode("p", "hello")
        self.assertEqual(node.to_html(), "<p>hello</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "click me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">click me</a>')

    def test_to_html_multiple_props(self):
        node = LeafNode(
            "a", "click", {"href": "https://example.com", "target": "_blank"}
        )
        result = node.to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith("<a "))
        self.assertTrue(result.endswith(">click</a>"))

    def test_to_html_no_tag_returns_raw_text(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_to_html_raises_when_value_is_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_children_always_none(self):
        node = LeafNode("span", "text")
        self.assertIsNone(node.children)

    def test_repr(self):
        node = LeafNode("p", "hello", {"class": "text"})
        self.assertEqual(
            repr(node),
            'LeafNode: tag="p", value="hello", props="{\'class\': \'text\'}"',
        )


if __name__ == "__main__":
    unittest.main()
