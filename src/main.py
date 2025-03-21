from build import clean, deploy_static_assets, build, list_files


def main():
    clean("./public")
    deploy_static_assets("./static", "./public")
    build("./content", "./public", "./template.html")

    list_files("./public")


if __name__ == "__main__":
    main()
