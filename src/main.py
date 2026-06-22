import os
import shutil
import sys

from copy_files import copy_files
from generate_page import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
    os.mkdir("docs/")

    copy_files("static/", "docs/")

    generate_pages_recursive("content/", "template.html", "docs/", basepath)

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
