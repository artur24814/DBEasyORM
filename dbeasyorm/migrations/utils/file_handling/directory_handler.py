import os


def create_directory_if_not_exists(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir
