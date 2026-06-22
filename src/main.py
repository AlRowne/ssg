import os
import shutil
import sys

from copy_files import copy_files
from generate_page import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) else "/"

    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public/")

    copy_files("static/", "public/")

    generate_pages_recursive(basepath, "template.html", "public/")

    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page(
    #     "content/blog/glorfindel/index.md",
    #     "template.html",
    #     "public/blog/glorfindel/index.html",
    # )
    # generate_page(
    #     "content/blog/majesty/index.md",
    #     "template.html",
    #     "public/blog/majesty/index.html",
    # )
    # generate_page(
    #     "content/blog/tom/index.md", "template.html", "public/blog/tom/index.html"
    # )


if __name__ == "__main__":
    main()
