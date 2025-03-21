import unittest
from parsing import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def pnodes(texttype: TextType, nodes: list[TextNode]) -> None:
    print(f"\n{texttype}:")
    for n in nodes:
        print("  ", n)


def text_to_textnodes(text: str) -> list[TextNode]:
    print("")
    print("*** text_to_textnodes")

    xforms = [
        (TextType.CODE, "`"),
        (TextType.BOLD, "**"),
        (TextType.ITALIC, "_"),
    ]

    root = TextNode(text, TextType.TEXT)
    print("root:", root)

    nodes = [root]
    for xform in xforms:
        texttype, delim = xform
        nodes = split_nodes_delimiter(nodes, delim, texttype)
        pnodes(texttype, nodes)

    nodes = split_nodes_image(nodes)
    pnodes(TextType.IMAGE, nodes)

    nodes = split_nodes_link(nodes)
    pnodes(TextType.LINK, nodes)

    return nodes


class Test_TextToTextnodes(unittest.TestCase):
    def test_parse_single_line(self):
        md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(md)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
