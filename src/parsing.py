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
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in range(0, len(old_nodes)):
        node = old_nodes[i]
        if delimiter in node.text:
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


def contains_image_or_link(text: str) -> bool:
    return "](" in text


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in range(0, len(old_nodes)):
        node = old_nodes[i]

        if contains_image_or_link(node.text):
            split = re.split(r"(!\[.+?\))", node.text)
            for line in split:
                if line == "":
                    continue
                elif line.startswith("!["):
                    [image] = extract_markdown_images(line)
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                else:
                    new_nodes.append(TextNode(line, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in range(0, len(old_nodes)):
        node = old_nodes[i]

        if contains_image_or_link(node.text):
            split = re.split(r"((?<!\!)\[.+?\))", node.text)

            for line in split:
                if line == "":
                    continue
                elif line.startswith("["):
                    [link] = extract_markdown_links(line)
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                else:
                    new_nodes.append(TextNode(line, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes
