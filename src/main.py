from ntpath import isfile
import os
import shutil
from pathlib import Path

from page import generate_page


def force_copy(src: str, dst: str) -> None:
    excluded = [".DS_Store"]

    if os.path.isfile(src):
        if os.path.basename(dst) not in excluded:
            shutil.copy(src, dst)
        return

    if os.path.isdir(src):
        print(f"d {src} -> {dst}")

        if not os.path.isdir(dst):
            os.mkdir(dst)

        files = os.listdir(src)

        for file in files:
            source = f"{src}/{file}"
            target = f"{dst}/{file}"
            force_copy(source, target)

    return


def clean(path: str):
    print(f"\nCleaning...")

    if os.path.exists(path):
        print(f"  found {path}")

        shutil.rmtree(path)

        if os.path.exists(path):
            raise FileExistsError(f"public directory should not exist: {path}")

        print(f"  removed {path}")

    else:
        print(f"  {path} not found ... nothing todo")

    print("done")


def tree(dir: str):
    path = Path(dir)
    for file in path.rglob("*"):
        if path.is_file():
            print(f"f {file}")
        else:
            print(f"d {file}")


def deploy_static_assets(src: str, dst: str):
    print("\nDeploying assets...")
    force_copy(src, dst)
    print("done")


def list_files(dir: str) -> None:
    print(f"\nListing files in {dir}...")

    path = Path(dir)
    for file in path.rglob("*"):
        filepath = f"{path.resolve()}/{file}"
        if os.path.isfile(file.resolve()):
            print(f"f {file}")
        else:
            print(f"d {file}")

    print("done")


def build():
    print("\nGenerating pages...")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


def main():
    clean("./public")
    deploy_static_assets("./static", "./public")
    build()
    list_files("./public")


if __name__ == "__main__":
    main()
