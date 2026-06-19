import re


def extract_markdown_images(text: str) -> list[tuple]:

    regex = r"!\[(.+?)\]\((.+?)\)"

    matches = re.findall(regex, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:

    # make sure [ is not preceeded by an ! as this would be an image
    regex = r"(?<!!)\[(.+?)\]\((.+?)\)"

    matches = re.findall(regex, text)
    return matches
