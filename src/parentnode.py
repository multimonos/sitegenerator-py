from typing import override
from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str | int] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("tag is cannot be empty")
        if self.children is None:
            raise ValueError("children cannot be empty")

        return self.collect_children(self)

    def collect_children(self, node: HTMLNode) -> str:
        if isinstance(node, LeafNode):
            return node.to_html()

        if node.children is None:  # this may not be correct
            return ""

        return (
            f"<{node.tag}>"
            + "".join(
                # easier to read
                [self.collect_children(child) for child in node.children]
                # fp is harder to read here
                # list(map(lambda child: self.collect_children(child), node.children))
            )
            + f"</{node.tag}>"
        )
