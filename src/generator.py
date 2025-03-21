from parsing import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def pnodes(texttype: TextType, nodes: list[TextNode]) -> None:
    print(f"\n{texttype}:")
    for n in nodes:
        print("  ", n)


def text_to_textnodes(text: str) -> list[TextNode]:
    # print("")
    # print("*** text_to_textnodes")

    xforms = [
        (TextType.CODE, "`"),
        (TextType.BOLD, "**"),
        (TextType.ITALIC, "_"),
    ]

    root = TextNode(text, TextType.TEXT)
    # print("root:", root)

    nodes = [root]
    for xform in xforms:
        texttype, delim = xform
        nodes = split_nodes_delimiter(nodes, delim, texttype)
        # pnodes(texttype, nodes)

    nodes = split_nodes_image(nodes)
    # pnodes(TextType.IMAGE, nodes)

    nodes = split_nodes_link(nodes)
    # pnodes(TextType.LINK, nodes)

    return nodes
