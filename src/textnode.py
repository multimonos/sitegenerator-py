from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    NORMAL = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{type(self).__name__}('{self.text}', {self.text_type}, {self.url})"


def text_node_to_html_node(node: TextNode) -> HTMLNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text, [])
        case TextType.BOLD:
            return LeafNode("b", node.text, [])
        case TextType.ITALIC:
            return LeafNode("i", node.text, [])
        case TextType.CODE:
            return LeafNode("code", node.text, [])
        case TextType.LINK:
            url = "" if node.url is None else node.url
            return LeafNode("a", node.text, [], {"href": url})
        case TextType.IMAGE:
            url = "" if node.url is None else node.url
            return LeafNode("img", "", [], {"src": url, "alt": node.text})
        case _:
            raise Exception("unknown text type")
