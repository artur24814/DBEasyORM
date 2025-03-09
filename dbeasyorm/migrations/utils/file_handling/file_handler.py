import os


def create_file_if_not_exists(dir: str, file_name: str, content: str) -> str:
    filepath = os.path.join(dir, file_name)
    if not os.path.exists(filepath):
        create_file(filepath, content)
    return filepath


def create_file(dir: str, file_name: str, content: str) -> str:
    filepath = os.path.join(dir, file_name)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath
