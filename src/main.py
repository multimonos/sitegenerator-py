import os
import shutil
from pathlib import Path

from page import generate_page


def force_copy(src: str, dst: str) -> None:
    if os.path.isfile(src):
        print(f"f {src} -> {dst}")
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
        print(file)


def deploy_static_assets(src: str, dst: str):
    print("\nDeploying assets...")
    force_copy(src, dst)
    print("done")


def list_files(dst: str) -> None:
    print(f"\ntarget:")
    tree(dst)
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
