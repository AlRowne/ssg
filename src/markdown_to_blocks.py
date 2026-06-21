import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:

    blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in blocks]
    new_blocks = [block for block in new_blocks if block != ""]

    return new_blocks


def block_to_block_type(block_of_markdown: str) -> BlockType:

    block = block_of_markdown.split("\n")

    if re.match(r"^#{1,6} ", block_of_markdown):
        return BlockType.HEADING
    if block_of_markdown.startswith("```") and block_of_markdown.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(block)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
