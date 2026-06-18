import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_single_child(self):
        node = ParentNode("p", [LeafNode("b", "bold")])
        self.assertEqual(node.to_html(), "<p><b>bold</b></p>")

    def test_to_html_multiple_children(self):
        node = ParentNode("p", [LeafNode("b", "bold"), LeafNode("i", "italic")])
        self.assertEqual(node.to_html(), "<p><b>bold</b><i>italic</i></p>")

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>text</p></div>')

    def test_to_html_nested(self):
        inner = ParentNode("p", [LeafNode("b", "bold")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><p><b>bold</b></p></div>")

    def test_to_html_raises_without_tag(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_raises_without_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_leaf_without_tag(self):
        node = ParentNode("p", [LeafNode(None, "raw text")])
        self.assertEqual(node.to_html(), "<p>raw text</p>")


if __name__ == "__main__":
    unittest.main()
