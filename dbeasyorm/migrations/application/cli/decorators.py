from functools import wraps
from .messages import print_line, print_error


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


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_error(e.message)
    return wrapper
