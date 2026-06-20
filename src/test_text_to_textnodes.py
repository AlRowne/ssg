import unittest

from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextnodes(unittest.TestCase):
    def test_combined_string(self):
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(markdown)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_unclosed_delimiter_raises(self):
        text = "This is just text, no markdown, or anything else in here. just a singe ` and maybe a * but thats not markdown!"

        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_empty_string(self):
        result = text_to_textnodes("")

        self.assertEqual(result, [])

    def test_truly_plain_text(self):
        result = text_to_textnodes("Just some normal words.")
        self.assertEqual(
            result, [TextNode("Just some normal words.", TextType.TEXT)]
        )

    def test_image_and_link_together(self):
        text = "![pic](https://i.img/p.png) then [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("pic", TextType.IMAGE, "https://i.img/p.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_markup_at_edges(self):
        result = text_to_textnodes("**start** middle `end`")
        self.assertEqual(
            result,
            [
                TextNode("start", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.CODE),
            ],
        )

    def test_adjacent_different_types(self):
        result = text_to_textnodes("**a**_b_")
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.BOLD),
                TextNode("b", TextType.ITALIC),
            ],
        )

    def test_unclosed_delimiter_message(self):
        with self.assertRaisesRegex(ValueError, "not closed"):
            text_to_textnodes("open **unclosed here")

    def test_multiple_images(self):
        text = "First Pic ![Placeholder](https://placehold.co/600x200/2B2F36/35D7BB?text=Your+Image+Here) second pic. ![Placeholder2](https://placehold2.co/600x200/2B2F36/35D7BB?text=Your+Image+Here)"
        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("First Pic ", TextType.TEXT),
                TextNode(
                    "Placeholder",
                    TextType.IMAGE,
                    "https://placehold.co/600x200/2B2F36/35D7BB?text=Your+Image+Here",
                ),
                TextNode(" second pic. ", TextType.TEXT),
                TextNode(
                    "Placeholder2",
                    TextType.IMAGE,
                    "https://placehold2.co/600x200/2B2F36/35D7BB?text=Your+Image+Here",
                ),
            ],
        )
