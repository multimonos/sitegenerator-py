import re
import os
from colorama import Style, Fore

from html import markdown_to_html_node
from format import fmt_dirname, fmt_filename, fmt_info, fmt_warn
from markdown import extract_title


class Document:
    title: str = ""
    content: str = ""


def generate_page(src: str, tplpath: str, dst: str) -> None:
    if not os.path.isfile(src):
        raise FileNotFoundError("page source not found: {src}")

    if not os.path.isfile(tplpath):
        raise FileNotFoundError("page template not found: {tplpath}")

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


def generate_pages_recursive(src: str, tplpath: str, dst: str) -> None:
    if os.path.isfile(src):
        _, ext = os.path.splitext(src)

        if ext == ".md":
            target = dst.replace(".md", ".html")
            print(fmt_filename(f"{src} -> {target}") + fmt_info(f" <> {tplpath}"))
            generate_page(src, tplpath, target)
        else:
            print(fmt_filename(src) + fmt_warn(" ... skipped "))
        return

    if os.path.isdir(src):
        print(fmt_dirname(f"{src} -> {dst}"))

        if not os.path.isdir(dst):
            os.mkdir(dst)

        files = os.listdir(src)

        for file in files:
            source = f"{src}/{file}"
            target = f"{dst}/{file}"
            generate_pages_recursive(source, tplpath, target)
    return
