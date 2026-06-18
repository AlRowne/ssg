import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_attributes_set(self):
        node = HTMLNode("p", "hello", [], {"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "text"})

    def test_repr(self):
        node = HTMLNode("a", "click", None, {"href": "https://example.com"})
        self.assertEqual(
            repr(node),
            'HTMLNode: tag="a", value="click", children="None", props="{\'href\': \'https://example.com\'}"',
        )

    def test_to_html_raises(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))

    def test_children_stored(self):
        child = HTMLNode("span", "inner")
        parent = HTMLNode("div", None, [child])
        self.assertEqual(len(parent.children), 1)
        self.assertIs(parent.children[0], child)


if __name__ == "__main__":
    unittest.main()
