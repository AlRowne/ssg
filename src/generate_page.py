import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.isfile(from_path):
        raise Exception(f"{from_path} is not a valid file")

    if not os.path.isfile(template_path):
        raise Exception(f"{template_path} is not a valid file")

    with open(from_path, "r") as file:
        markdown = file.read()

    with open(template_path, "r") as file:
        template_file = file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    final_html = template_file.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)

    if not os.path.isdir(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        _ = f.write(final_html)
