from typing import override

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def __repr__(self) -> str:
        return f'LeafNode: tag="{self.tag}", value="{self.value}", props="{self.props}"'

    @override
    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
