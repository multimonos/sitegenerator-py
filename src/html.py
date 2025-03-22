import re

from blocks import BlockType, block_to_blocktype, markdown_to_blocks
from generator import text_to_textnodes
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node


def heading_from_block(block: str) -> ParentNode:
    matches: list[str] = re.findall(r"^(#+)\s", block.strip())
    if len(matches) != 1:
        raise ValueError("invalid heading level")
    level = len(matches[0])
    textnodes = text_to_textnodes(re.sub(r"^#+\s+", "", block))
    leaves = list(map(text_node_to_html_node, textnodes))
    parent = ParentNode(f"h{level}", leaves)
    return parent


def paragraph_from_block(block: str) -> ParentNode:
    textnodes = text_to_textnodes(block)
    leaves = list(map(text_node_to_html_node, textnodes))
    return ParentNode("p", leaves)


def code_from_block(block: str) -> ParentNode:
    codestr = block.replace("```", "").lstrip()
    children: list[HTMLNode] = [LeafNode("code", codestr)]
    parent = ParentNode("pre", children)
    return parent


def unordered_list_from_block(block: str) -> ParentNode:
    lines = [x.strip() for x in re.split(r"\-\s", block.strip()) if x != ""]
    text_nodes = list(map(text_to_textnodes, lines))
    items: list[HTMLNode] = [
        ParentNode("li", list(map(text_node_to_html_node, x))) for x in text_nodes
    ]
    parent = ParentNode("ul", items)
    return parent


def ordered_list_from_block(block: str) -> ParentNode:
    lines = [x.strip() for x in re.split(r"[0-9]\.\s", block.strip()) if x != ""]
    text_nodes = list(map(text_to_textnodes, lines))
    items: list[HTMLNode] = [
        ParentNode("li", list(map(text_node_to_html_node, x))) for x in text_nodes
    ]
    parent = ParentNode("ol", items)
    return parent


def blockquote_from_block(block: str) -> ParentNode:
    lines = [x.strip() for x in re.split(r"\>\s", block.strip()) if x != ""]
    textnodes = list(map(text_to_textnodes, lines))
    children = [list(map(text_node_to_html_node, nodes)) for nodes in textnodes]
    paragraphs: list[HTMLNode] = [ParentNode("p", nodes) for nodes in children]
    parent = ParentNode("blockquote", paragraphs)
    return parent


def markdown_to_html_node(doc: str) -> HTMLNode:
    # convert to blocks
    blocks: list[str] = markdown_to_blocks(doc)
    nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_blocktype(block)

        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_from_block(block))

            case BlockType.CODE:
                nodes.append(code_from_block(block))

            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_from_block(block))

            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_from_block(block))

            case BlockType.QUOTE:
                nodes.append(blockquote_from_block(block))

            case BlockType.HEADING:
                nodes.append(heading_from_block(block))

            case _:
                print("\n<<<<<<<<<<<<<<> missing {block_type} <>>>>>>>>>>>>>>>>>")
                pass

    root = ParentNode("div", nodes)

    return root
