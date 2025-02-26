from .config import get_registered_operators


def apply_sql_operator(col_query: str, value) -> str:
    try:
        col, operator_name = col_query.split('__')
    except ValueError:
        col, operator_name = col_query, None

    current_oper = get_operator(operator_name)
    return current_oper().apply(col, value)


def get_operator(operator_name: str):
    all_registered_operators = get_registered_operators()
    for name, oper in all_registered_operators.items():
        if operator_name == name:
            return oper

    return all_registered_operators['default']
