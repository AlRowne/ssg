import os
import shutil

from copy_files import copy_files


def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public/")

    copy_files("static/", "public/")


if __name__ == "__main__":
    main()
