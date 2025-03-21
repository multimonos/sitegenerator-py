import unittest

from blocks import BlockType, block_to_blocktype, markdown_to_blocks
from generator import text_to_textnodes
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node


def create_block_htmlnode(block_type: BlockType, children: list[HTMLNode]):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", children)

        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            return ParentNode("ol", children)

        case BlockType.CODE:
            return ParentNode("code", children)

        case _:
            return None


def code_node_from_block(block: str):
    codestr = block.replace("```", "").lstrip()
    return ParentNode("pre", [LeafNode("code", codestr)])


def markdown_to_html_node(doc: str):
    # convert to blocks
    blocks: list[str] = markdown_to_blocks(doc)
    nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_blocktype(block)
        child_textnodes = text_to_textnodes(block)
        child_htmlnodes = list(map(text_node_to_html_node, child_textnodes))

        if block_type == BlockType.CODE:
            block_node = code_node_from_block(block)
            nodes.append(block_node)
        else:
            block_node = create_block_htmlnode(block_type, child_htmlnodes)
            if not block_node is None:
                nodes.append(block_node)

    root = ParentNode("div", nodes)

    return root


class Test_markdown_to_html(unittest.TestCase):
    # @unittest.skip("fo")
    def test_paragraph_multiline(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p></div>",
        )

    # @unittest.skip("fo")
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # @unittest.skip("fo")
    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
