import os
import shutil
from pathlib import Path
from colorama import Style, Fore
from page import generate_page, generate_pages_recursive
from format import fmt_filename, fmt_dirname, fmt_title


def force_copy(src: str, dst: str) -> None:
    excluded = [".DS_Store"]

    if os.path.isfile(src):
        if os.path.basename(dst) not in excluded:
            shutil.copy(src, dst)
        return

    if os.path.isdir(src):
        print(fmt_dirname(f"{src} -> {dst}"))

        if not os.path.isdir(dst):
            os.mkdir(dst)

        files = os.listdir(src)

        for file in files:
            source = f"{src}/{file}"
            target = f"{dst}/{file}"
            force_copy(source, target)

    return


def clean(path: str):
    print(fmt_title("Cleaning..."))

    if os.path.exists(path):
        print(f"  found {path}")

        shutil.rmtree(path)

        if os.path.exists(path):
            raise FileExistsError(f"public directory should not exist: {path}")

        print(f"  removed {path}")

    else:
        print(f"  {path} not found ... nothing todo")


def deploy_static_assets(src: str, dst: str):
    print(fmt_title("Deploying assets..."))
    force_copy(src, dst)


def list_files(dir: str) -> None:
    print(fmt_title(f"Listing files in {dir}..."))

    path = Path(dir)
    for file in path.rglob("*"):
        if os.path.isfile(file.resolve()):
            print(fmt_filename(file))
        else:
            print(fmt_dirname(file))


def build(src: str, dst: str, template_path: str) -> None:
    print(fmt_title("Generating pages..."))
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive(src, template_path, dst)
