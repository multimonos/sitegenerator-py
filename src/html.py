from typing import Any
import unittest
import re

from blocks import BlockType, block_to_blocktype, markdown_to_blocks
from generator import pnodes, text_to_textnodes
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node
import textnode


def pchilds(l: list[HTMLNode], tag="children"):
    print(f"\n<> {tag}")
    for x in l:
        print(x)


def create_block_htmlnode(block_type: BlockType, children: list[HTMLNode]):
    match block_type:
        case BlockType.PARAGRAPH:
            pchilds(children)
            return ParentNode("p", children)

        case BlockType.UNORDERED_LIST:
            # print("\nchildren<>", children, children[0].value)
            # pchilds(children)
            # nodes = evolve_list_children(children)
            # print("\nli-nodes:", nodes)
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            return ParentNode("ol", children)

        case BlockType.CODE:
            codestr = block.replace("```", "").lstrip()
            return ParentNode("pre", [LeafNode("code", codestr)])
            return ParentNode("code", children)

        case _:
            return None


def evolve_list_children(nodes):
    return nodes

    # lines = text.strip().split("\n")
    # return [TextNode("li", re.sub(r"^(\-|)\s+", "", text)) for text in lines]


def code_node_from_block(block: str) -> HTMLNode:
    codestr = block.replace("```", "").lstrip()
    return ParentNode("pre", [LeafNode("code", codestr)])


def list_node_from_block(block: str) -> HTMLNode:
    pass


def evolve_listitems(nodes: list[LeafNode]) -> list[LeafNode]:
    leaves = []
    for n in nodes:
        if n.tag is not None:
            leaves.append(n)

    return leaves


def paragraph_from_block(block: str) -> ParentNode:
    text_nodes = text_to_textnodes(block)
    leaves = list(map(text_node_to_html_node, text_nodes))
    return ParentNode("p", leaves)


def code_from_block(block: str) -> ParentNode:
    codestr = block.replace("```", "").lstrip()
    children = [LeafNode("code", codestr)]
    parent = ParentNode("pre", children)
    return parent


def unordered_list_from_block(block: str) -> ParentNode:
    lines = [x.strip() for x in re.split(r"\-\s", block.strip()) if x != ""]
    text_nodes = list(map(text_to_textnodes, lines))
    items = [ParentNode("li", list(map(text_node_to_html_node, x))) for x in text_nodes]
    parent = ParentNode("ul", items)
    return parent


def ordered_list_from_block(block: str) -> ParentNode:
    lines = [x.strip() for x in re.split(r"[0-9]\.\s", block.strip()) if x != ""]
    text_nodes = list(map(text_to_textnodes, lines))
    items = [ParentNode("li", list(map(text_node_to_html_node, x))) for x in text_nodes]
    parent = ParentNode("ol", items)
    return parent


def markdown_to_html_node(doc: str) -> HTMLNode:
    # convert to blocks
    blocks: list[str] = markdown_to_blocks(doc)
    nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_blocktype(block)
        # text_nodes = text_to_textnodes(block)
        # html_nodes = list(map(text_node_to_html_node, text_nodes))

        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_from_block(block))

            case BlockType.CODE:
                nodes.append(code_from_block(block))

            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_from_block(block))

            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_from_block(block))

            case _:
                pass

        # if block_type == BlockType.CODE:
        #     block_node = code_node_from_block(block)
        #     nodes.append(block_node)
        # elif block_type == BlockType.UNORDERED_LIST:
        #     block_node = list_node_from_block(block)
        #     nodes.append(block_node)
        # else:
        # block_node = create_block_htmlnode(block_type, html_nodes)
        # if not block_node is None:
        #     nodes.append(block_node)
        #
    root = ParentNode("div", nodes)

    return root
