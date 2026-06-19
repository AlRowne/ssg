import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "![cat](https://example.com/cat.png)"
        self.assertEqual(extract_markdown_images(text), [("cat", "https://example.com/cat.png")])

    def test_multiple_images(self):
        text = "![a](url1) some text ![b](url2)"
        self.assertEqual(extract_markdown_images(text), [("a", "url1"), ("b", "url2")])

    def test_no_images(self):
        text = "just plain text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_link_not_extracted_as_image(self):
        text = "[not an image](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_image_among_links(self):
        text = "[link](url1) ![img](url2)"
        self.assertEqual(extract_markdown_images(text), [("img", "url2")])

    def test_image_with_spaces_in_alt(self):
        text = "![my cute cat](cat.png)"
        self.assertEqual(extract_markdown_images(text), [("my cute cat", "cat.png")])

    def test_returns_list_of_tuples(self):
        result = extract_markdown_images("![x](y)")
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)

    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "[boot.dev](https://boot.dev)"
        self.assertEqual(extract_markdown_links(text), [("boot.dev", "https://boot.dev")])

    def test_multiple_links(self):
        text = "[a](url1) and [b](url2)"
        self.assertEqual(extract_markdown_links(text), [("a", "url1"), ("b", "url2")])

    def test_no_links(self):
        text = "just plain text"
        self.assertEqual(extract_markdown_links(text), [])

    def test_image_not_extracted_as_link(self):
        text = "![alt](https://example.com/img.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_among_images(self):
        text = "![img](img_url) [link](link_url)"
        self.assertEqual(extract_markdown_links(text), [("link", "link_url")])

    def test_mixed_images_and_links(self):
        text = "See ![cat](cat.png) and visit [boot.dev](https://boot.dev) now"
        self.assertEqual(extract_markdown_links(text), [("boot.dev", "https://boot.dev")])

    def test_link_with_spaces_in_anchor(self):
        text = "[click here](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("click here", "https://example.com")])

    def test_returns_list_of_tuples(self):
        result = extract_markdown_links("[x](y)")
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)

    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_multiple_images_no_links(self):
        text = "![a](1) ![b](2) ![c](3)"
        self.assertEqual(extract_markdown_links(text), [])


if __name__ == "__main__":
    unittest.main()
