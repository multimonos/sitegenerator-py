from typing import override
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str | int] | None = None,
        is_open_tag: bool = True,
    ) -> None:
        super().__init__(tag, value, None, props)
        self.is_open_tag: bool = is_open_tag

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return str(self.value)

        props = "" if self.props is None else " " + self.props_to_html()

        if self.is_open_tag:
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{props} />"
