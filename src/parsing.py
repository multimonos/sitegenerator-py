from textnode import TextNode, TextType
import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # use the negative look behind to ensure no prefixed ! with `(?<!\!)`
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_delimiter(
    old_nodes: list[object], delimiter: str, text_type: TextType
) -> list[object]:
    nodes = list(old_nodes)

    new_nodes: list[object] = []

    for i in range(0, len(nodes)):
        node = old_nodes[i]
        if isinstance(node, TextNode) and delimiter in node.text:
            texts = node.text.split(delimiter)

            textnodes = [
                TextNode(texts[0], node.text_type, node.url),
                TextNode(texts[1], text_type, node.url),
                TextNode(texts[2], node.text_type, node.url),
            ]

            # replace item at i with the items in textnodes
            new_nodes.extend(textnodes)
        else:
            new_nodes.append(node)

    return new_nodes
