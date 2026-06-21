from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            url = text_node.url
            if url is None:
                raise ValueError("LINK text node requires a URL")
            return LeafNode("a", text_node.text, {"href": url})
        case TextType.IMAGE:
            url = text_node.url
            if url is None:
                raise ValueError("IMAGE text node requires a URL")

            return LeafNode("img", "", {"src": url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
