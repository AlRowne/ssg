def extract_title(markdown: str):
    if not markdown.strip().startswith("# "):
        raise ValueError("markdown doesn't start with a title")

    return markdown.lstrip("# ").strip().split("\n")[0]
