import os
import shutil
from pathlib import Path


def main():
    clean("./public")
    deploy_static_assets("./static", "./public")
    build()


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

    print("\nValidating...")
    print(f"\nsource:")
    tree(src)
    print(f"\ntarget:")
    tree(dst)
    print("done")


def build():
    pass


if __name__ == "__main__":
    main()
