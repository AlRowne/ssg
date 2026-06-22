from htmlnode import HTMLNode, ParentNode
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType
from textnode_to_html import text_node_to_html_node


def markdown_to_html_node(markdown: str) -> ParentNode:

    blocks = markdown_to_blocks(markdown)
    block_nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_num = len(block) - len(block.lstrip("#"))
                block = block.lstrip("#").lstrip()
                children = text_to_children(block)
                parent = ParentNode(f"h{heading_num}", children)

            case BlockType.PARAGRAPH:
                block = " ".join(block.split("\n"))
                children = text_to_children(block)
                parent = ParentNode("p", children)

            case BlockType.CODE:
                block = block[4:-3]
                node = TextNode(block, TextType.TEXT)
                html_node = text_node_to_html_node(node)
                code = ParentNode("code", [html_node])
                parent = ParentNode("pre", [code])

            case BlockType.QUOTE:
                # split the block at the newlines, then strip every line of "> ", then join it with spaces
                block = [line.lstrip(">").strip() for line in block.split("\n")]
                block = " ".join(block)

                children = text_to_children(block)
                parent = ParentNode("blockquote", children)

            case BlockType.UNORDERED_LIST:
                block = [line.lstrip("-").strip() for line in block.split("\n")]
                children: list[HTMLNode] = []
                for line in block:
                    children.append(ParentNode("li", text_to_children(line)))
                parent = ParentNode("ul", children)

            case BlockType.ORDERED_LIST:
                block = [line.split(". ", 1)[1] for line in block.split("\n")]
                children = []
                for line in block:
                    children.append(ParentNode("li", text_to_children(line)))
                parent = ParentNode("ol", children)

        block_nodes.append(parent)

    return ParentNode("div", block_nodes)


def text_to_children(text: str) -> list[HTMLNode]:

    text_nodes = text_to_textnodes(text)
    children: list[HTMLNode] = [text_node_to_html_node(node) for node in text_nodes]

    return children
