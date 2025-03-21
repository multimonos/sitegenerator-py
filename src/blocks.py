from enum import Enum
import re
from typing import override


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(doc: str) -> list[str]:
    if doc.strip() == "":
        return []

    # replace multiple blank lines with a single blank line
    doc = re.sub(r"\n{2,}", "\n\n", doc)

    lines = doc.strip().split("\n")

    # add a blank line to force the pushing of block onto blocks
    lines.append("")

    blocks: list[str] = []
    block = ""

    for line in lines:
        txt = line.strip()

        if txt == "":
            blocks.append(block.strip())
            block = ""
        else:
            block += "\n" + txt

    # print("blocks:", blocks)
    return blocks


def block_to_blocktype(block: str) -> BlockType:
    if block.startswith("> "):
        return BlockType.QUOTE

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif re.match(r"^\#{1,6}\s", block):
        return BlockType.HEADING

    elif block.startswith("- "):
        lines = block.split("\n")
        found = list(filter(lambda line: line.startswith("- "), lines))
        if len(lines) == len(found):
            return BlockType.UNORDERED_LIST

    elif re.match(r"^[0-9]\.\s", block):
        lines = block.split("\n")
        found = list(filter(lambda line: re.match(r"^[0-9]\.\s", line), lines))
        if len(lines) == len(found):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
