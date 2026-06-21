from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    @override
    def __repr__(self) -> str:
        return f'HTMLNode: tag="{self.tag}", value="{self.value}", children="{self.children}", props="{self.props}"'

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented in subclasses")

    def props_to_html(self) -> str:
        props = ""
        if self.props:
            for key, value in self.props.items():
                props += f' {key}="{value}"'

        return props


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    @override
    def __repr__(self) -> str:
        return f'LeafNode: tag="{self.tag}", value="{self.value}", props="{self.props}"'

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"

        return html
