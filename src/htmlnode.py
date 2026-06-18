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
