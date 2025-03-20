from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str | int] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str | int] | None = props

    @override
    def __repr__(self) -> str:
        return f"{type(self).__name__}(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self) -> str:
        raise NotImplemented

    def props_to_html(self) -> str:
        if isinstance(self.props, dict):
            return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
        return ""
