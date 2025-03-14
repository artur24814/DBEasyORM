from functools import wraps
from .messages import print_line


def adding_separation_characters(color, character: str = "=", print_message_fnc=None):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            print_line(color, char=character)
            test_func(*args, **kwargs)
            if print_message_fnc:
                print_message_fnc()
            print_line(color, char=character)
        return wrapper
    return decorator
