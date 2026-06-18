from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: delimiter '{delimiter}' not closed in '{node.text}'"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue
            current_type = text_type if i % 2 != 0 else TextType.TEXT
            new_nodes.append(TextNode(part, current_type))

    return new_nodes
