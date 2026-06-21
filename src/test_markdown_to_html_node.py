import unittest

from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_single_paragraph(self):
        md = "hello world"
        node = markdown_to_html_node(md)

        self.assertEqual(node.to_html(), "<div><p>hello world</p></div>")

    def test_paragraph_with_inline(self):
        md = "hello **world** and _friends_ with `code`"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><p>hello <b>world</b> and <i>friends</i> with <code>code</code></p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "first paragraph\n\nsecond **bold** paragraph"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><p>first paragraph</p><p>second <b>bold</b> paragraph</p></div>",
        )


    def test_code_block_no_inline_parsing(self):
        md = "```\nThis is _not_ italic and **not** bold\n```"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><pre><code>This is _not_ italic and **not** bold\n</code></pre></div>",
        )


    def test_quote(self):
        md = "> first line\n> second **bold** line"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>first line second <b>bold</b> line</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- first\n- second with _italic_\n- third"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first</li><li>second with <i>italic</i></li><li>third</li></ul></div>",
        )


    def test_ordered_list(self):
        md = "1. first\n2. second with **bold**\n3. third"
        node = markdown_to_html_node(md)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second with <b>bold</b></li><li>third</li></ol></div>",
        )

    def test_ordered_list_multi_digit(self):
        md = "\n".join(f"{i}. item {i}" for i in range(1, 12))
        node = markdown_to_html_node(md)
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 12))

        self.assertEqual(node.to_html(), f"<div><ol>{expected_items}</ol></div>")


if __name__ == "__main__":
    unittest.main()
