import re


def insert_pattern_into_str(pattern, replacement, str):
    return re.sub(pattern, replacement, str, count=1)
