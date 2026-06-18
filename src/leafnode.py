from typing import override

from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str, value: str | None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def to_html(self):
        return super().to_html()
