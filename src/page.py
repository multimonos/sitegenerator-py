from ntpath import isfile
import re
import os

from html import markdown_to_html_node
from markdown import extract_title


class Document:
    title: str = ""
    content: str = ""


def generate_page(src: str, tplpath: str, dst: str) -> None:
    if not os.path.isfile(src):
        raise FileNotFoundError("page source not found: {src}")

    if not os.path.isfile(tplpath):
        raise FileNotFoundError("page template not found: {tplpath}")

    print(f"{tplpath} | {src} -> {dst}")

    with open(src, "r", encoding="latin1") as f:
        markdown = f.read()

    doc = Document()
    doc.title = extract_title(markdown)
    doc.content = markdown_to_html_node(markdown).to_html()

    with open(tplpath, "r") as f:
        tpl = f.read()

    # sub
    html = re.sub(r"\{\{\s*Title\s*\}\}", doc.title, tpl)
    html = re.sub(r"\{\{\s*Content\s*\}\}", doc.content, html)

    with open(dst, "w+") as f:
        f.write(html)
