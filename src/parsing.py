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
    """if delimiter is found then replace the captured node with a node of type TextType"""

    new_nodes: list[TextNode] = []

    # this only loops once becasue the "old_nodes" always has length 1 for a block
    # so, if the delimiter exists more than 1 time we cannot catch it

    needle = re.compile("(" + re.escape(delimiter) + ".+?" + re.escape(delimiter) + ")")

    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)

        else:
            tokens = [x for x in re.split(needle, node.text) if x != ""]
            for tok in tokens:
                if delimiter in tok:
                    value = tok.replace(delimiter, "")
                    new_nodes.append(TextNode(value, text_type, node.url))
                else:
                    new_nodes.append(TextNode(tok, node.text_type, node.url))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for i in range(0, len(old_nodes)):
        node = old_nodes[i]

        if "](" in node.text:
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

        if "](" in node.text:
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
