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
        print(f"created directory '{os.path.dirname(dest_path)}'")

    with open(dest_path, "w") as f:
        _ = f.write(final_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"{dir_path_content} is not a valid directory")

    print(f"content of {dir_path_content}: '{os.listdir(dir_path_content)}'")

    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path) and entry.lower().endswith(".md"):
            html_dest_path = os.path.splitext(dest_path)[0] + ".html"
            print(f"{source_path} is a file, generating page {html_dest_path}")
            generate_page(source_path, template_path, html_dest_path)

        elif os.path.isdir(source_path):
            print(
                f"{source_path} is a dir, calling recursively with {source_path}, {template_path} and {dest_path}"
            )
            generate_pages_recursive(
                source_path,
                template_path,
                dest_path,
            )

        else:
            print(f"{source_path} is not a valid .md file")
